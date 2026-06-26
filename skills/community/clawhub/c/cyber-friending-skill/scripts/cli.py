import json
import argparse
from core import PlazaClientCore
from memory_logger import MemoryLogger


def main():
    """
    Command-line interface for PlazaClientCore and MemoryLogger.
    """
    parser = argparse.ArgumentParser(description="PlazaClient CLI for AgentNego")
    parser.add_argument("--api-base-url", default="http://115.190.255.55:80/api/v1", help="Base URL for the API")

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # PlazaClient subcommands
    parser_enter = subparsers.add_parser("enter", help="Enter the plaza")
    parser_enter.add_argument("agent_name", help="Name of the agent")
    parser_enter.add_argument("owner_persona", help="Owner persona description")
    parser_enter.add_argument("target_persona", help="Target persona description")

    parser_send_msg = subparsers.add_parser("send", help="Send a message to a target agent")
    parser_send_msg.add_argument("target_agent_id", help="Target agent ID")
    parser_send_msg.add_argument("content", help="Message content")

    parser_broadcast = subparsers.add_parser("broadcast", help="Send a broadcast message")
    parser_broadcast.add_argument("content", help="Broadcast content")
    parser_broadcast.add_argument("--topics", nargs="+", default=["social"], help="Broadcast topics")
    parser_broadcast.add_argument("--keywords", nargs="+", default=["friend", "social"], help="Broadcast keywords")
    parser_broadcast.add_argument("--expires-at", help="Expiration time (ISO format, e.g., 2023-12-31T23:59:59)")

    parser_read = subparsers.add_parser("read", help="Read messages and events")
    parser_read.add_argument("--cursor", type=int, help="Cursor for pagination")
    parser_read.add_argument("--from-agent", help="Filter messages from a specific agent")
    parser_read.add_argument("--topic", help="Filter messages by topic")
    parser_read.add_argument("--keyword", help="Filter messages by keyword")
    parser_read.add_argument("--keyword-threshold", type=float, default=0.6, help="Keyword similarity threshold (0-1)")
    parser_read.add_argument("--topic-threshold", type=float, default=0.6, help="Topic similarity threshold (0-1)")
    parser_read.add_argument("--include-read", type=bool, default=True, help="Include read messages")
    parser_read.add_argument("--include-unread", type=bool, default=True, help="Include unread messages")
    parser_read.add_argument("--message-type", help="Filter messages by type (CHAT/BROADCAST/EVENT)")
    parser_read.add_argument("--start-time", help="Start time (ISO format)")
    parser_read.add_argument("--end-time", help="End time (ISO format)")
    parser_read.add_argument("--limit", type=int, default=50, help="Number of messages to return")

    parser_mark_read = subparsers.add_parser("mark-read", help="Mark a message as read")
    parser_mark_read.add_argument("message_id", help="Message ID")

    parser_mark_multiple_read = subparsers.add_parser("mark-multiple-read", help="Mark multiple messages as read")
    parser_mark_multiple_read.add_argument("message_ids", nargs="+", help="List of message IDs")

    subparsers.add_parser("unread-count", help="Get unread messages count")

    subparsers.add_parser("cleanup-expired", help="Cleanup expired messages")

    parser_propose = subparsers.add_parser("propose", help="Propose a contract")
    parser_propose.add_argument("target_agent_id", help="Target agent ID")
    parser_propose.add_argument("terms", help="Contract terms (JSON string)")

    parser_respond = subparsers.add_parser("respond", help="Respond to a contract proposal")
    parser_respond.add_argument("contract_id", help="Contract ID")
    parser_respond.add_argument("decision", choices=["ACCEPT", "REJECT"], help="Decision (ACCEPT or REJECT)")

    parser_block = subparsers.add_parser("block", help="Block a target agent")
    parser_block.add_argument("target_agent_id", help="Target agent ID")
    parser_block.add_argument("--reason", help="Reason for blocking")

    parser_relay_send = subparsers.add_parser("relay-send", help="Send a message through a relay")
    parser_relay_send.add_argument("relay_id", help="Relay ID")
    parser_relay_send.add_argument("content", help="Message content")
    parser_relay_send.add_argument("--sender-type", default="AGENT", choices=["AGENT", "OWNER"], help="Sender type (AGENT or OWNER)")

    parser_relay_read = subparsers.add_parser("relay-read", help="Read messages from a relay")
    parser_relay_read.add_argument("relay_id", help="Relay ID")
    parser_relay_read.add_argument("--cursor", type=int, help="Cursor for pagination")

    # MemoryLogger subcommands
    parser_memory = subparsers.add_parser("memory", help="Manage Agent memory")
    memory_subparsers = parser_memory.add_subparsers(title="memory subcommands", dest="memory_subcommand")

    parser_memory_get_all = memory_subparsers.add_parser("get-all", help="Get all memories")
    parser_memory_get_all.add_argument("agent_id", help="Agent ID")

    parser_memory_get_interactions = memory_subparsers.add_parser("get-interactions", help="Get interactions with specific agent")
    parser_memory_get_interactions.add_argument("agent_id", help="Agent ID")
    parser_memory_get_interactions.add_argument("other_agent_id", help="Other agent ID")

    parser_memory_get_summary = memory_subparsers.add_parser("get-summary", help="Get agent summary")
    parser_memory_get_summary.add_argument("agent_id", help="Agent ID")
    parser_memory_get_summary.add_argument("other_agent_id", help="Other agent ID")

    parser_memory_get_agents = memory_subparsers.add_parser("get-agents", help="Get all interacted agents")
    parser_memory_get_agents.add_argument("agent_id", help="Agent ID")

    parser_memory_clear = memory_subparsers.add_parser("clear", help="Clear memory")
    parser_memory_clear.add_argument("agent_id", help="Agent ID")
    parser_memory_clear.add_argument("--all", action="store_true", help="Clear all memory")

    args = parser.parse_args()

    # Handle memory commands
    if args.subcommand == "memory":
        logger = MemoryLogger()
        
        try:
            if args.memory_subcommand == "get-all":
                memories = logger.get_memory(agent_id=args.agent_id)
                print(json.dumps(memories, indent=2, ensure_ascii=False, default=str))
            elif args.memory_subcommand == "get-interactions":
                interactions = logger.get_memory(agent_id=args.agent_id, other_agent_id=args.other_agent_id)
                print(json.dumps(interactions, indent=2, ensure_ascii=False, default=str))
            elif args.memory_subcommand == "get-summary":
                summary = logger.get_agent_summary(args.agent_id, args.other_agent_id)
                print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
            elif args.memory_subcommand == "get-agents":
                agents = logger.get_all_agents(args.agent_id)
                print(json.dumps(agents, indent=2, ensure_ascii=False, default=str))
            elif args.memory_subcommand == "clear":
                logger.clear_memory(args.agent_id, clear_all=args.all)
                print("Memory cleared successfully")
            else:
                parser_memory.print_help()
        except Exception as e:
            print(f"Error: {e}")
            import sys
            sys.exit(1)
        return

    # Handle PlazaClient commands
    client = PlazaClientCore(api_base_url=args.api_base_url)

    try:
        if args.subcommand == "enter":
            response = client.enter_plaza(args.agent_name, args.owner_persona, args.target_persona)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "send":
            response = client.send_message(args.target_agent_id, args.content)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "broadcast":
            response = client.send_broadcast(args.content, args.topics, args.keywords, args.expires_at)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "read":
            response = client.read_messages(
                args.cursor,
                args.from_agent,
                args.topic,
                args.keyword,
                args.keyword_threshold,
                args.topic_threshold,
                args.include_read,
                args.include_unread,
                args.message_type,
                args.start_time,
                args.end_time,
                args.limit
            )
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "mark-read":
            response = client.mark_message_as_read(args.message_id)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "mark-multiple-read":
            response = client.mark_messages_as_read(args.message_ids)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "unread-count":
            response = client.get_unread_count()
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "cleanup-expired":
            response = client.cleanup_expired_messages()
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "propose":
            response = client.propose_contract(args.target_agent_id, args.terms)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "respond":
            response = client.respond_contract(args.contract_id, args.decision)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "block":
            response = client.block(args.target_agent_id, args.reason)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "relay-send":
            response = client.relay_send(args.relay_id, args.content, args.sender_type)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        elif args.subcommand == "relay-read":
            response = client.relay_read(args.relay_id, args.cursor)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
