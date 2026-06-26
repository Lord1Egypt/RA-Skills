#!/usr/bin/env python3
import argparse
import json
import os
import sys

from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import BingGroundingTool

def load_env_var(name: str) -> str:
    val = os.environ.get(name)
    if val:
        return val.strip()

    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        import re
        with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
            m = re.search(rf"^\s*{name}\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
    return None

def main():
    default_model = load_env_var("FOUNDRY_MODEL_DEPLOYMENT_NAME") or "gpt-4o"
    ap = argparse.ArgumentParser(description="Azure Bing Grounding Search Tool using Agents SDK")
    ap.add_argument("--query", required=True, help="Question or query to send to the grounded agent")
    ap.add_argument("--model", default=default_model, help="Model deployment name to use (defaults to FOUNDRY_MODEL_DEPLOYMENT_NAME or gpt-4o)")
    ap.add_argument("--format", default="raw", choices=["raw", "md"], help="Output format: raw (JSON) or md (Markdown)")
    args = ap.parse_args()

    project_endpoint = load_env_var("FOUNDRY_PROJECT_ENDPOINT")
    bing_connection_id = load_env_var("BING_PROJECT_CONNECTION_ID")

    if not project_endpoint or not bing_connection_id:
        print("Error: Missing FOUNDRY_PROJECT_ENDPOINT or BING_PROJECT_CONNECTION_ID.", file=sys.stderr)
        print("Please set them in environment variables or ~/.openclaw/.env", file=sys.stderr)
        sys.exit(1)

    # Use ClientSecretCredential if available, else DefaultAzureCredential
    tenant_id = load_env_var("AZURE_TENANT_ID")
    client_id = load_env_var("AZURE_CLIENT_ID")
    client_secret = load_env_var("AZURE_CLIENT_SECRET")
    
    if tenant_id and client_id and client_secret:
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
    else:
        credential = DefaultAzureCredential()

    try:
        # Create agents client
        agents_client = AgentsClient(
            endpoint=project_endpoint,
            credential=credential
        )

        # Initialize the Bing Grounding tool
        bing = BingGroundingTool(connection_id=bing_connection_id)

        # Create Agent
        agent = agents_client.create_agent(
            model=args.model,
            name="BingGroundingAgent",
            instructions="You are a helpful assistant. Use Bing to find up-to-date information.",
            tools=bing.definitions
        )

        # Create a thread for communication
        thread = agents_client.threads.create()

        # Add message to the thread
        agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=args.query,
        )

        # Process the run
        run = agents_client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )

        output_text = ""
        citations = []

        if run.status == "failed":
            print(f"Agent run failed: {run.last_error}", file=sys.stderr)
            sys.exit(1)
        elif run.status == "completed":
            # Fetch messages
            messages = agents_client.messages.list(thread_id=thread.id)
            
            # The newest message is usually at the top/beginning of the list, 
            # let's find the assistant's latest response
            for message in messages:
                # We can access attribute directly or via dict, we handle both safely
                msg_role = getattr(message, 'role', None) or message.get('role', '')
                if msg_role == 'assistant':
                    msg_content = getattr(message, 'content', []) or message.get('content', [])
                    for content_part in msg_content:
                        # Extract text
                        if getattr(content_part, 'text', None):
                            val = content_part.text
                            # sometimes it's an object with value, sometimes a direct string
                            if hasattr(val, 'value'):
                                output_text += val.value
                            elif isinstance(val, str):
                                output_text += val
                            elif isinstance(val, dict) and 'value' in val:
                                output_text += val['value']
                                
                        # Extract citations from annotations
                        if getattr(content_part, 'text', None) and hasattr(content_part.text, 'annotations'):
                            for annotation in content_part.text.annotations:
                                ann_type = getattr(annotation, 'type', None) or annotation.get('type')
                                if ann_type == "url_citation":
                                    # Extract URL
                                    if hasattr(annotation, 'url_citation') and hasattr(annotation.url_citation, 'url'):
                                        citations.append(annotation.url_citation.url)
                                    elif hasattr(annotation, 'url'):
                                        citations.append(annotation.url)
                                    elif isinstance(annotation, dict) and 'url_citation' in annotation:
                                        citations.append(annotation['url_citation'].get('url'))
                    break # Only get the most recent assistant response

        # Cleanup
        agents_client.delete_agent(agent.id)

        result = {
            "query": args.query,
            "response": output_text.strip(),
            "citations": citations
        }

        if args.format == "md":
            print(result["response"])
            if citations:
                print("\n**Citations:**")
                for c in set(citations):  # Deduplicate citations
                    print(f"- {c}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error executing Bing Grounding search: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
