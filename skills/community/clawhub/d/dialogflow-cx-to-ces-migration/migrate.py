"""
Dialogflow CX → Customer Engagement Suite (CES) Conversational Agents Migration Tool
Full migration: Flows, Pages, Intents, Entity Types, Webhooks, Parameters → CES format

Usage:
    python migrate.py --project genaiguruyoutube --agent-id 3736c564-5b3b-4f93-bbb2-367e7f04e4e8
    python migrate.py --project genaiguruyoutube --agent-id <id> --output ./output --dry-run
"""

import argparse
import json
import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field, asdict

from google.auth import default
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import dialogflowcx_v3beta1 as dfcx

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ─── Retry helper ─────────────────────────────────────────────────────────────

def retry(fn, max_attempts=4, base_delay=1.5):
    """Exponential backoff retry for Google API calls."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except (GoogleAPICallError, RetryError) as e:
            if attempt == max_attempts - 1:
                raise
            wait = base_delay * (2 ** attempt)
            log.warning(f"  API error (attempt {attempt+1}/{max_attempts}): {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

# ─── Data models ──────────────────────────────────────────────────────────────

@dataclass
class CESParameter:
    name: str
    entity_type: str
    required: bool
    prompts: list[str] = field(default_factory=list)

@dataclass
class CESPage:
    name: str
    cx_id: str
    entry_messages: list[str] = field(default_factory=list)
    parameters: list[CESParameter] = field(default_factory=list)
    routes: list[dict] = field(default_factory=list)
    event_handlers: list[dict] = field(default_factory=list)

@dataclass
class CESSubAgent:
    name: str
    cx_flow_id: str
    description: str
    instructions: list[str] = field(default_factory=list)
    pages: list[CESPage] = field(default_factory=list)
    tools_referenced: list[str] = field(default_factory=list)

@dataclass
class CESTool:
    name: str
    cx_webhook_id: str
    description: str
    endpoint: str
    auth_type: str = "NONE"

@dataclass
class CESMigrationResult:
    source_agent_name: str
    source_agent_id: str
    source_project: str
    root_agent_instructions: list[str] = field(default_factory=list)
    sub_agents: list[CESSubAgent] = field(default_factory=list)
    tools: list[CESTool] = field(default_factory=list)
    entity_types: list[dict] = field(default_factory=list)
    golden_evals: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    migration_stats: dict = field(default_factory=dict)

# ─── Core migration logic ─────────────────────────────────────────────────────

class DialogflowCXMigrator:
    def __init__(self, project: str, agent_id: str, location: str = "global"):
        self.project = project
        self.agent_id = agent_id
        self.location = location
        self.agent_name = f"projects/{project}/locations/{location}/agents/{agent_id}"

        try:
            self.creds, _ = default()
        except DefaultCredentialsError as e:
            log.error(f"GCP credentials not found: {e}")
            sys.exit(1)

        self.agents_client    = dfcx.AgentsClient(credentials=self.creds)
        self.flows_client     = dfcx.FlowsClient(credentials=self.creds)
        self.pages_client     = dfcx.PagesClient(credentials=self.creds)
        self.intents_client   = dfcx.IntentsClient(credentials=self.creds)
        self.entities_client  = dfcx.EntityTypesClient(credentials=self.creds)
        self.webhooks_client  = dfcx.WebhooksClient(credentials=self.creds)
        self.test_cases_client = dfcx.TestCasesClient(credentials=self.creds)

    def _get_text_messages(self, fulfillment) -> list[str]:
        """Extract all text messages from a Dialogflow CX fulfillment."""
        messages = []
        for msg in fulfillment.messages:
            if msg.text and msg.text.text:
                messages.extend(msg.text.text)
        return [m for m in messages if m.strip()]

    def _resolve_target(self, route, flow_map: dict, page_map: dict) -> str:
        """Resolve a transition route target to a human-readable name."""
        if route.target_flow:
            flow_id = route.target_flow.split("/")[-1]
            return f"flow:{flow_map.get(flow_id, flow_id)}"
        if route.target_page:
            page_id = route.target_page.split("/")[-1]
            if page_id == "END_SESSION":
                return "END_SESSION"
            if page_id == "END_FLOW":
                return "END_FLOW"
            if page_id == "START_PAGE":
                return "START_PAGE"
            return f"page:{page_map.get(page_id, page_id)}"
        return "PASSTHROUGH"

    def migrate(self) -> CESMigrationResult:
        log.info(f"🚀 Starting migration for agent: {self.agent_name}")

        # Step 1: Fetch agent metadata
        agent = retry(lambda: self.agents_client.get_agent(name=self.agent_name))
        log.info(f"  ✅ Agent: {agent.display_name} (lang={agent.default_language_code})")

        result = CESMigrationResult(
            source_agent_name=agent.display_name,
            source_agent_id=self.agent_id,
            source_project=self.project,
        )

        # Step 2: Fetch all flows
        flows = list(retry(lambda: self.flows_client.list_flows(parent=self.agent_name)))
        flow_map = {f.name.split("/")[-1]: f.display_name for f in flows}
        log.info(f"  ✅ Flows: {len(flows)}")

        # Step 3: Fetch all intents (for route condition resolution)
        intents = list(retry(lambda: self.intents_client.list_intents(parent=self.agent_name)))
        intent_map = {i.name: i.display_name for i in intents}
        log.info(f"  ✅ Intents: {len(intents)}")

        # Step 4: Fetch entity types
        entity_types = list(retry(lambda: self.entities_client.list_entity_types(parent=self.agent_name)))
        log.info(f"  ✅ Entity Types: {len(entity_types)}")
        for et in entity_types:
            result.entity_types.append({
                "name": et.display_name,
                "kind": et.kind.name,
                "auto_expansion": et.auto_expansion_mode.name,
                "entities": [
                    {"value": e.value, "synonyms": list(e.synonyms)}
                    for e in et.entities
                ]
            })

        # Step 5: Fetch webhooks → CES Tools
        webhooks = list(retry(lambda: self.webhooks_client.list_webhooks(parent=self.agent_name)))
        log.info(f"  ✅ Webhooks: {len(webhooks)}")
        for wh in webhooks:
            endpoint = ""
            auth_type = "NONE"
            if wh.generic_web_service.uri:
                endpoint = wh.generic_web_service.uri
                if wh.generic_web_service.allowed_ca_certs:
                    auth_type = "MTLS"
            result.tools.append(CESTool(
                name=wh.display_name.lower().replace(" ", "_").replace("-", "_"),
                cx_webhook_id=wh.name.split("/")[-1],
                description=f"Migrated from Dialogflow CX webhook: {wh.display_name}",
                endpoint=endpoint,
                auth_type=auth_type,
            ))
        tool_map = {t.cx_webhook_id: t.name for t in result.tools}

        # Step 6: Build root agent instructions from Default Start Flow + intents
        root_instructions = self._build_root_instructions(agent, flows, intents, flow_map)
        result.root_agent_instructions = root_instructions

        # Step 7: Migrate each non-default flow → CES Sub-Agent
        page_map: dict[str, str] = {}

        for flow in flows:
            flow_id = flow.name.split("/")[-1]
            log.info(f"  📦 Migrating flow: {flow.display_name}")

            pages = list(retry(lambda fn=flow.name: self.pages_client.list_pages(parent=fn)))
            for p in pages:
                page_map[p.name.split("/")[-1]] = p.display_name

            ces_pages = []
            tools_used = set()

            for page in pages:
                # Entry fulfillment messages
                entry_msgs = self._get_text_messages(page.entry_fulfillment)

                # Check if webhook used in entry fulfillment
                if page.entry_fulfillment.webhook:
                    wh_id = page.entry_fulfillment.webhook.split("/")[-1]
                    if wh_id in tool_map:
                        tools_used.add(tool_map[wh_id])

                # Parameters (form fields)
                ces_params = []
                for param in page.form.parameters:
                    prompts = []
                    for fill_behavior in [param.fill_behavior]:
                        for prompt_msg in fill_behavior.initial_prompt_fulfillment.messages:
                            if prompt_msg.text and prompt_msg.text.text:
                                prompts.extend(prompt_msg.text.text)
                    ces_params.append(CESParameter(
                        name=param.display_name,
                        entity_type=param.entity_type.split("/")[-1] if "/" in param.entity_type else param.entity_type,
                        required=param.required,
                        prompts=[p for p in prompts if p.strip()],
                    ))

                # Transition routes
                ces_routes = []
                for route in page.transition_routes:
                    condition = ""
                    if route.intent:
                        condition = f"intent:{intent_map.get(route.intent, route.intent.split('/')[-1])}"
                    elif route.condition:
                        condition = f"condition:{route.condition}"

                    fulfillment_msgs = self._get_text_messages(route.trigger_fulfillment)

                    # Webhook in fulfillment
                    if route.trigger_fulfillment.webhook:
                        wh_id = route.trigger_fulfillment.webhook.split("/")[-1]
                        if wh_id in tool_map:
                            tools_used.add(tool_map[wh_id])

                    ces_routes.append({
                        "condition": condition,
                        "messages": fulfillment_msgs,
                        "target": self._resolve_target(route, flow_map, page_map),
                    })

                # Event handlers
                ces_handlers = []
                for handler in page.event_handlers:
                    msgs = self._get_text_messages(handler.trigger_fulfillment)
                    ces_handlers.append({
                        "event": handler.event,
                        "messages": msgs,
                        "target": self._resolve_target(handler, flow_map, page_map),
                    })

                ces_pages.append(CESPage(
                    name=page.display_name,
                    cx_id=page.name.split("/")[-1],
                    entry_messages=entry_msgs,
                    parameters=ces_params,
                    routes=ces_routes,
                    event_handlers=ces_handlers,
                ))

            # Build sub-agent instructions from pages
            sub_instructions = self._pages_to_instructions(flow.display_name, ces_pages)

            if flow_id == "00000000-0000-0000-0000-000000000000":
                # Default Start Flow merges into root
                result.root_agent_instructions.extend(sub_instructions)
                continue

            result.sub_agents.append(CESSubAgent(
                name=flow.display_name.lower().replace(" ", "_").replace("&", "and").replace("-", "_"),
                cx_flow_id=flow_id,
                description=f"Handles: {flow.display_name}",
                instructions=sub_instructions,
                pages=ces_pages,
                tools_referenced=list(tools_used),
            ))

        # Step 8: Fetch and convert test cases → golden evals CSV
        test_cases = list(retry(lambda: self.test_cases_client.list_test_cases(parent=self.agent_name)))
        log.info(f"  ✅ Test Cases: {len(test_cases)}")
        result.golden_evals = self._convert_test_cases(test_cases, intent_map)

        # Stats
        result.migration_stats = {
            "flows": len(flows),
            "sub_agents": len(result.sub_agents),
            "intents": len(intents),
            "entity_types": len(entity_types),
            "webhooks": len(webhooks),
            "tools": len(result.tools),
            "test_cases": len(test_cases),
            "golden_evals": len(result.golden_evals),
            "warnings": len(result.warnings),
        }

        return result

    def _build_root_instructions(self, agent, flows, intents, flow_map: dict) -> list[str]:
        """Generate root agent instructions listing available sub-agents."""
        instructions = [
            f"You are {agent.display_name}, a helpful conversational agent.",
            f"You communicate in {agent.default_language_code}.",
            "",
            "## Available capabilities (delegate to sub-agents):",
        ]
        for flow in flows:
            flow_id = flow.name.split("/")[-1]
            if flow_id == "00000000-0000-0000-0000-000000000000":
                continue
            safe_name = flow.display_name.lower().replace(" ", "_").replace("&", "and").replace("-", "_")
            instructions.append(f"- **{safe_name}**: {flow.display_name}")

        instructions += [
            "",
            "## Routing instructions:",
            "- Greet the user warmly and identify their intent.",
            "- Delegate to the appropriate sub-agent based on the user's request.",
            "- If unsure, ask a clarifying question.",
            "- If the user wants to end: say goodbye and end the session.",
        ]

        # Add intent-based routing hints
        instructions.append("")
        instructions.append("## Intent routing hints:")
        for intent in intents:
            if intent.display_name.startswith("Default"):
                continue
            if intent.training_phrases:
                samples = [tp.parts[0].text for tp in intent.training_phrases[:2] if tp.parts]
                instructions.append(f"- '{intent.display_name}': triggered by phrases like {samples}")

        return instructions

    def _pages_to_instructions(self, flow_name: str, pages: list[CESPage]) -> list[str]:
        """Convert CX pages to natural language instructions for a CES sub-agent."""
        instructions = [f"# {flow_name}", ""]

        for page in pages:
            instructions.append(f"## Step: {page.name}")

            if page.entry_messages:
                instructions.append(f"Say: \"{page.entry_messages[0]}\"")

            if page.parameters:
                instructions.append("Collect the following information from the user:")
                for param in page.parameters:
                    req = "required" if param.required else "optional"
                    prompt = f" Ask: \"{param.prompts[0]}\"" if param.prompts else ""
                    instructions.append(f"  - **{param.name}** ({param.entity_type}, {req}).{prompt}")

            if page.routes:
                instructions.append("Transition rules:")
                for route in page.routes:
                    if route["condition"] or route["messages"]:
                        cond = route["condition"] or "after collecting parameters"
                        msgs = f" Respond: \"{route['messages'][0]}\"" if route["messages"] else ""
                        target = route["target"]
                        instructions.append(f"  - When {cond}:{msgs} → go to {target}")

            if page.event_handlers:
                for handler in page.event_handlers:
                    msgs = f" Say: \"{handler['messages'][0]}\"" if handler["messages"] else ""
                    instructions.append(f"  - On event '{handler['event']}':{msgs}")

            instructions.append("")

        return instructions

    def _convert_test_cases(self, test_cases, intent_map: dict) -> list[dict]:
        """Convert Dialogflow CX test cases to CES golden eval format."""
        evals = []
        for tc in test_cases:
            if not tc.test_case_conversation_turns:
                continue
            turns = []
            turn_idx = 1
            for conversation_turn in tc.test_case_conversation_turns:
                user_input = conversation_turn.user_input
                virtual_agent_output = conversation_turn.virtual_agent_output

                if user_input and user_input.input:
                    inp = user_input.input
                    if inp.text and inp.text.text:
                        turns.append({
                            "turn_index": turn_idx,
                            "action_type": "INPUT_TEXT",
                            "text_content": inp.text.text,
                        })

                if virtual_agent_output and virtual_agent_output.text_responses:
                    for resp in virtual_agent_output.text_responses:
                        for text in resp.text:
                            turns.append({
                                "turn_index": turn_idx,
                                "action_type": "EXPECTATION_TEXT",
                                "response_agent": "root_agent",
                                "text_content": text,
                            })
                turn_idx += 1

            if turns:
                evals.append({
                    "display_name": tc.display_name or f"test_case_{len(evals)+1}",
                    "description": tc.notes or "",
                    "tags": "migrated_from_cx",
                    "turns": turns,
                })

        # If no test cases had conversation turns, synthesize basic smoke tests from intents
        if not evals:
            evals = self._synthesize_smoke_tests()

        return evals

    def _synthesize_smoke_tests(self) -> list[dict]:
        """Generate basic golden evals from intent training phrases when no test cases exist."""
        intents = list(retry(lambda: self.intents_client.list_intents(parent=self.agent_name)))
        evals = []
        for intent in intents:
            if intent.display_name.startswith("Default"):
                continue
            if not intent.training_phrases:
                continue
            sample_phrase = None
            for tp in intent.training_phrases[:1]:
                parts_text = "".join(p.text for p in tp.parts)
                if parts_text.strip():
                    sample_phrase = parts_text.strip()
                    break
            if not sample_phrase:
                continue
            evals.append({
                "display_name": f"smoke_{intent.display_name.lower().replace(' ', '_')}",
                "description": f"Synthetic smoke test for intent: {intent.display_name}",
                "tags": "synthetic;migrated_from_cx",
                "turns": [
                    {
                        "turn_index": 1,
                        "action_type": "INPUT_TEXT",
                        "text_content": sample_phrase,
                    },
                    {
                        "turn_index": 1,
                        "action_type": "EXPECTATION_TEXT",
                        "response_agent": "root_agent",
                        "text_content": "",  # Blank = any response accepted
                        "expectation_note": f"Agent should handle {intent.display_name} intent",
                    },
                ],
            })
        return evals

# ─── Output formatters ────────────────────────────────────────────────────────

def write_ces_agent_json(result: CESMigrationResult, output_dir: Path):
    """Write the CES agent definition as a JSON file (importable structure)."""
    ces_agent = {
        "displayName": result.source_agent_name,
        "defaultLanguageCode": "en",
        "timeZone": "America/Los_Angeles",
        "description": f"Migrated from Dialogflow CX agent {result.source_agent_id}",
        "globalInstruction": "\n".join(result.root_agent_instructions),
        "agents": [],
        "tools": [],
    }

    for sub in result.sub_agents:
        ces_agent["agents"].append({
            "displayName": sub.name,
            "description": sub.description,
            "instruction": "\n".join(sub.instructions),
            "tools": sub.tools_referenced,
        })

    for tool in result.tools:
        ces_agent["tools"].append({
            "displayName": tool.name,
            "description": tool.description,
            "openapiTool": {
                "textSchema": json.dumps({
                    "openapi": "3.0.0",
                    "info": {"title": tool.name, "version": "1.0.0"},
                    "servers": [{"url": tool.endpoint or "https://REPLACE_WITH_ENDPOINT"}],
                    "paths": {
                        "/": {
                            "post": {
                                "summary": tool.description,
                                "operationId": tool.name,
                                "requestBody": {
                                    "content": {"application/json": {"schema": {"type": "object"}}}
                                },
                                "responses": {"200": {"description": "Success"}}
                            }
                        }
                    }
                }, indent=2),
                "authentication": {"authType": tool.auth_type},
            }
        })

    out_path = output_dir / "ces_agent.json"
    out_path.write_text(json.dumps(ces_agent, indent=2), encoding="utf-8")
    log.info(f"  📄 Written: {out_path}")


def write_golden_evals_csv(result: CESMigrationResult, output_dir: Path):
    """Write golden evaluations in CES batch upload CSV format."""
    import csv
    out_path = output_dir / "golden_evals.csv"

    fieldnames = [
        "display_name", "turn_index", "action_type",
        "text_content", "response_agent",
        "description", "tags", "evaluation_id",
        "tool_name", "tool_call_args_json", "expectation_note"
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for eval_def in result.golden_evals:
            first = True
            for turn in eval_def["turns"]:
                row = {k: "" for k in fieldnames}
                row["turn_index"] = turn["turn_index"]
                row["action_type"] = turn["action_type"]
                row["text_content"] = turn.get("text_content", "")
                row["response_agent"] = turn.get("response_agent", "")
                if first:
                    row["display_name"] = eval_def["display_name"]
                    row["description"] = eval_def.get("description", "")
                    row["tags"] = eval_def.get("tags", "")
                    first = False
                writer.writerow(row)

    log.info(f"  📄 Written: {out_path}")


def write_entity_types_json(result: CESMigrationResult, output_dir: Path):
    out_path = output_dir / "entity_types.json"
    out_path.write_text(json.dumps(result.entity_types, indent=2), encoding="utf-8")
    log.info(f"  📄 Written: {out_path}")


def write_migration_report(result: CESMigrationResult, output_dir: Path):
    lines = [
        "# Dialogflow CX → CES Migration Report",
        "",
        f"**Source Agent:** {result.source_agent_name} (`{result.source_agent_id}`)",
        f"**Project:** {result.source_project}",
        "",
        "## Migration Stats",
        "| Item | Count |",
        "|------|-------|",
    ]
    for k, v in result.migration_stats.items():
        lines.append(f"| {k.replace('_', ' ').title()} | {v} |")

    lines += [
        "",
        "## Sub-Agents Created",
    ]
    for sub in result.sub_agents:
        lines.append(f"### `{sub.name}`")
        lines.append(f"- **CX Flow:** `{sub.cx_flow_id}`")
        lines.append(f"- **Description:** {sub.description}")
        lines.append(f"- **Pages migrated:** {len(sub.pages)}")
        lines.append(f"- **Tools used:** {sub.tools_referenced or 'none'}")
        lines.append("")

    if result.tools:
        lines.append("## Tools (from Webhooks)")
        for t in result.tools:
            lines.append(f"- **{t.name}**: `{t.endpoint or 'ENDPOINT NOT SET'}` ({t.auth_type})")
        lines.append("")

    if result.warnings:
        lines.append("## ⚠️ Warnings")
        for w in result.warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines += [
        "## Output Files",
        "| File | Description |",
        "|------|-------------|",
        "| `ces_agent.json` | CES agent definition (importable via REST API or Console) |",
        "| `golden_evals.csv` | Test cases in CES batch evaluation CSV format |",
        "| `entity_types.json` | Entity type definitions for manual re-creation in CES |",
        "| `migration_report.md` | This report |",
        "",
        "## Next Steps",
        "1. Review `ces_agent.json` and update tool endpoints in the `tools` section",
        "2. Import agent via CES Console: Console > Import Agent > Upload JSON",
        "3. Upload `golden_evals.csv` via: Evaluate tab > + Add test case > Golden > Upload file",
        "4. Re-create entity types from `entity_types.json` as CES does not have a direct import path",
        "5. Update webhook URLs in each tool definition to point to your live endpoints",
        "6. Run evaluation suite and review pass rates",
    ]

    out_path = output_dir / "migration_report.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"  📄 Written: {out_path}")


# ─── CLI entrypoint ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Dialogflow CX → CES Conversational Agents Migration Tool")
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--agent-id", required=True, help="Dialogflow CX agent UUID")
    parser.add_argument("--location", default="global", help="Agent location (default: global)")
    parser.add_argument("--output", default="./migration_output", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Fetch data but don't write files")
    args = parser.parse_args()

    output_dir = Path(args.output)
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    migrator = DialogflowCXMigrator(
        project=args.project,
        agent_id=args.agent_id,
        location=args.location,
    )

    result = migrator.migrate()

    log.info("")
    log.info("📊 Migration Summary:")
    for k, v in result.migration_stats.items():
        log.info(f"  {k}: {v}")

    if args.dry_run:
        log.info("\n⚠️  Dry run — no files written.")
        print(json.dumps({"stats": result.migration_stats, "warnings": result.warnings}, indent=2))
        return

    log.info("\n✍️  Writing output files...")
    write_ces_agent_json(result, output_dir)
    write_golden_evals_csv(result, output_dir)
    write_entity_types_json(result, output_dir)
    write_migration_report(result, output_dir)

    log.info(f"\n✅ Migration complete. Output in: {output_dir.resolve()}")
    if result.warnings:
        log.warning(f"⚠️  {len(result.warnings)} warnings — see migration_report.md")


if __name__ == "__main__":
    main()
