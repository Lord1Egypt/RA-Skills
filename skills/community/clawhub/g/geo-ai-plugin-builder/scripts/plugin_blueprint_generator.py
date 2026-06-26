"""
plugin_blueprint_generator.py

This helper module defines a simple, opinionated structure for
GEO-aware AI plugin/tool blueprints. It is not meant to be a
full framework, but rather a concrete reference for how to
organize information when designing tools programmatically.

You do not have to run this script directly; you can mirror
its data structures inside your own codebase or internal specs.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: Dict[str, Any]
    response: Dict[str, Any]


@dataclass
class PluginBlueprint:
    plugin_name: str
    geo_role: str
    primary_job: str
    target_platforms: List[str]
    priority: str
    tools: List[ToolSchema]
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the blueprint."""
        data = asdict(self)
        return data


def generate_plugin_blueprint(
    plugin_name: str,
    primary_job: str,
    geo_role: str,
    target_platforms: Optional[List[str]] = None,
    priority: str = "high",
    notes: Optional[str] = None,
) -> PluginBlueprint:
    """
    Create a minimal PluginBlueprint with a single empty ToolSchema stub.

    You can then fill in the ToolSchema fields manually. This function
    exists primarily as an example for how to structure plugin metadata.
    """
    if target_platforms is None:
        target_platforms = ["ChatGPT", "Claude", "Perplexity", "Gemini"]

    tool_stub = ToolSchema(
        name=f"{plugin_name}_core_tool",
        description=f"Core tool for: {primary_job}",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        response={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    )

    blueprint = PluginBlueprint(
        plugin_name=plugin_name,
        geo_role=geo_role,
        primary_job=primary_job,
        target_platforms=target_platforms,
        priority=priority,
        tools=[tool_stub],
        notes=notes,
    )
    return blueprint


def example_blueprint() -> Dict[str, Any]:
    """
    Return an example blueprint for documentation or quick experiments.
    """
    bp = generate_plugin_blueprint(
        plugin_name="marketing_analytics_insights",
        primary_job="Help users analyze campaign performance and suggest optimizations.",
        geo_role="evaluation_and_optimization",
        target_platforms=["ChatGPT", "Claude"],
        priority="high",
        notes=(
            "Designed as a high-intent tool for existing customers and "
            "qualified leads who want deep insight into campaign ROI."
        ),
    )
    return bp.to_dict()


if __name__ == "__main__":
    import json

    example = example_blueprint()
    print(json.dumps(example, indent=2))

"""
plugin_blueprint_generator.py

This helper module defines data structures and utilities that act as a
mental model for turning high-level "jobs to be done" into concrete AI
plugin/tool specifications.

The GEO AI Plugin Builder skill does not need to literally execute this
code. Instead, treat the structures and examples here as a reference for
how to shape outputs: small, composable, and implementation-ready.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: List[ToolParameter]
    response_fields: List[ToolParameter]

    def to_openai_json(self) -> Dict[str, Any]:
        """Return an OpenAI-style JSON schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    p.name: {
                        "type": p.type,
                        "description": p.description,
                    }
                    for p in self.parameters
                },
                "required": [p.name for p in self.parameters if p.required],
            },
        }

    def response_example(self) -> Dict[str, Any]:
        """
        Produce a stub example of the response shape.

        This is intentionally generic; callers should customize values and
        add domain-specific examples when using it inside the skill.
        """
        example: Dict[str, Any] = {}
        for field in self.response_fields:
            # Provide very lightweight defaults based on type.
            if field.type == "string":
                example[field.name] = f"<{field.name} string>"
            elif field.type == "number":
                example[field.name] = 0
            elif field.type == "boolean":
                example[field.name] = False
            elif field.type == "array":
                example[field.name] = []
            else:
                example[field.name] = None
        return example


@dataclass
class PluginBlueprint:
    """
    High-level blueprint for an AI plugin or tool group.
    """

    name: str
    primary_job: str
    geo_role: str
    target_platforms: List[str]
    tools: List[ToolSchema]

    def summary(self) -> Dict[str, Any]:
        """
        Return a compact summary suitable for catalogs or overview tables.
        """
        return {
            "name": self.name,
            "primary_job": self.primary_job,
            "geo_role": self.geo_role,
            "target_platforms": self.target_platforms,
            "tool_names": [tool.name for tool in self.tools],
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the entire blueprint into primitive Python types.
        """
        return {
            "name": self.name,
            "primary_job": self.primary_job,
            "geo_role": self.geo_role,
            "target_platforms": self.target_platforms,
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "parameters": [asdict(p) for p in t.parameters],
                    "response_fields": [asdict(p) for p in t.response_fields],
                }
                for t in self.tools
            ],
        }


def example_blueprint() -> PluginBlueprint:
    """
    Return a minimal example blueprint for documentation and testing.
    """
    parameters = [
        ToolParameter(
            name="website_url",
            type="string",
            description="Public URL of the landing page to analyze.",
        ),
        ToolParameter(
            name="target_audience",
            type="string",
            description="Short description of the intended audience segment.",
        ),
    ]

    response_fields = [
        ToolParameter(
            name="summary",
            type="string",
            description="Concise summary of the page content.",
        ),
        ToolParameter(
            name="geo_opportunities",
            type="array",
            description="List of GEO opportunities identified on the page.",
        ),
    ]

    analysis_tool = ToolSchema(
        name="analyze_landing_page_for_geo",
        description=(
            "Analyze a landing page and suggest GEO-optimized messaging, "
            "FAQs, and potential AI tools that could be built from it."
        ),
        parameters=parameters,
        response_fields=response_fields,
    )

    return PluginBlueprint(
        name="geo_landing_page_analyzer",
        primary_job="Turn key landing pages into GEO-aware AI analysis tools.",
        geo_role="Discovery and optimization of high-intent pages.",
        target_platforms=["ChatGPT", "Claude", "Internal Agents"],
        tools=[analysis_tool],
    )


__all__ = [
    "ToolParameter",
    "ToolSchema",
    "PluginBlueprint",
    "example_blueprint",
]

