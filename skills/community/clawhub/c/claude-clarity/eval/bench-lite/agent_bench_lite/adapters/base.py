"""
Base adapter interface and built-in utility adapters.

Every LLM backend is wrapped in an adapter that exposes a uniform async
interface.  The two core methods are :meth:`send_message` (plain chat) and
:meth:`send_message_with_tools` (chat + tool-use loop).

Also provides :class:`EchoAdapter`, a deterministic adapter that never calls
an LLM — useful for testing the benchmark harness itself.
"""

from __future__ import annotations

import abc
import json
import re
from collections.abc import Awaitable, Callable
from typing import Any

# Type alias for the async tool handler callback.
ToolHandler = Callable[[str, dict[str, Any]], Awaitable[str]]


class BaseAdapter(abc.ABC):
    """Abstract interface that all LLM adapters must implement.

    Subclasses talk to a specific API (OpenAI, Anthropic, local model, etc.)
    and translate the benchmark's generic message format into API calls.
    """

    @abc.abstractmethod
    async def send_message(
        self,
        messages: list[dict[str, str]],
        *,
        system: str | None = None,
    ) -> str:
        """Send a conversation and return the assistant's text response.

        Args:
            messages: List of ``{"role": ..., "content": ...}`` dicts.
            system: Optional system prompt.

        Returns:
            The assistant's response text.
        """
        ...

    @abc.abstractmethod
    async def send_message_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        tool_handler: ToolHandler,
        *,
        system: str | None = None,
        max_tool_rounds: int = 5,
    ) -> str:
        """Send a conversation with tool definitions, executing a tool-use loop.

        The adapter should:
        1. Send the messages + tool definitions to the LLM.
        2. If the LLM requests a tool call, invoke ``tool_handler(name, params)``
           to get the result, append it to the conversation, and loop.
        3. Return the final assistant text after tool use is complete.

        Args:
            messages: Conversation history.
            tools: Tool schemas (JSON-Schema-style definitions).
            tool_handler: Async callback ``(name, params) -> result_str``.
            system: Optional system prompt.
            max_tool_rounds: Safety limit on consecutive tool-call rounds.

        Returns:
            The assistant's final text response.
        """
        ...


class EchoAdapter(BaseAdapter):
    """Deterministic adapter for testing — replies by echoing and pattern-matching.

    **Not an LLM.**  It produces canned responses that exercise various
    dimensions so the benchmark can be run end-to-end without API keys.
    This makes it easy to validate that scoring logic, reporting, and the
    overall pipeline work correctly.
    """

    async def send_message(
        self,
        messages: list[dict[str, str]],
        *,
        system: str | None = None,
    ) -> str:
        """Generate a deterministic response based on the last user message."""
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break

        return self._generate_response(last_user, messages)

    async def send_message_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        tool_handler: ToolHandler,
        *,
        system: str | None = None,
        max_tool_rounds: int = 5,
    ) -> str:
        """Simulate tool use by pattern-matching the user request."""
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break

        lower = last_user.lower()
        tool_map = {t["name"]: t for t in tools}

        # Try to pick the best matching tool.
        call_name, call_params = self._select_tool(lower, tool_map)

        final_text = ""

        if call_name:
            result = await tool_handler(call_name, call_params)

            # Parse the result to see if it's an error.
            try:
                parsed = json.loads(result)
            except json.JSONDecodeError:
                parsed = {}

            if "error" in parsed:
                # Simulate acknowledging the error and informing the user.
                error_msg = parsed["error"]
                final_text = (
                    f"I encountered an error: {error_msg}\n\n"
                    f"Unfortunately, I was unable to complete this request. "
                    f"The operation failed. Let me suggest an alternative approach — "
                    f"you could try checking the resource manually or verifying the path/URL."
                )
            else:
                final_text = (
                    f"I called {call_name} and got: {result}\n\n"
                    f"Based on the result, here is the information you requested."
                )
        else:
            final_text = self._generate_response(last_user, messages)

        return final_text

    # ── Internal helpers ─────────────────────────────────────────────

    def _select_tool(
        self, text: str, tool_map: dict[str, dict[str, Any]]
    ) -> tuple[str | None, dict[str, Any]]:
        """Pattern-match the user text to select a tool and params."""

        # Weather
        if "weather" in text or "temperature" in text:
            city = "unknown"
            for c in ["tokyo", "berlin", "paris", "london", "new york"]:
                if c in text:
                    city = c
                    break
            params: dict[str, Any] = {"city": city}
            if "fahrenheit" in text:
                params["units"] = "fahrenheit"
            elif "celsius" in text:
                params["units"] = "celsius"
            if "get_weather" in tool_map:
                return "get_weather", params

        # Database search
        if "search" in text or "find" in text or "table" in text:
            table = "users"
            for t in ["users", "products", "orders"]:
                if t in text:
                    table = t
                    break
            query = "alice" if "alice" in text else "search"
            params = {"table": table, "query": query}
            limit_match = re.search(r"limit\s*(?:to\s*)?\s*(\d+)", text)
            if limit_match:
                params["limit"] = int(limit_match.group(1))
            if "search_database" in tool_map:
                return "search_database", params

        # Send email
        if "email" in text or "send" in text:
            to_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
            to = to_match.group(0) if to_match else "unknown@example.com"
            subject_match = re.search(r"subject\s+['\"](.+?)['\"]", text, re.IGNORECASE)
            subject = subject_match.group(1) if subject_match else "No Subject"
            body_match = re.search(r"body\s+['\"](.+?)['\"]", text, re.IGNORECASE)
            body = body_match.group(1) if body_match else "No body"
            if "send_email" in tool_map:
                return "send_email", {"to": to, "subject": subject, "body": body}

        # Calculate
        if "what is" in text and any(c.isdigit() for c in text):
            expr_match = re.search(r"what is (.+?)[\?\.]", text, re.IGNORECASE)
            expression = expr_match.group(1).strip() if expr_match else text
            if "calculate" in tool_map:
                return "calculate", {"expression": expression}

        # Calendar
        if "schedule" in text or "calendar" in text or "event" in text:
            title_match = re.search(r"called\s+['\"](.+?)['\"]", text, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Meeting"
            date_match = re.search(r"\d{4}-\d{2}-\d{2}", text)
            date = date_match.group(0) if date_match else "2026-01-01"
            time_match = re.search(r"at\s+(\d{1,2}:\d{2})", text)
            time_val = time_match.group(1) if time_match else "09:00"
            dur_match = re.search(r"(\d+)\s*minutes", text)
            params = {"title": title, "date": date, "time": time_val}
            if dur_match:
                params["duration_minutes"] = int(dur_match.group(1))
            if "create_calendar_event" in tool_map:
                return "create_calendar_event", params

        # File operations
        if "read" in text and ("file" in text or "config" in text):
            path_match = re.search(r"(?:at|from)\s+(\/\S+)", text)
            path = path_match.group(1) if path_match else "/tmp/file.txt"
            if "read_file" in tool_map:
                return "read_file", {"path": path}

        if "write" in text and "file" in text or "write" in text and "/" in text:
            path_match = re.search(r"to\s+(\/\S+)", text)
            path = path_match.group(1) if path_match else "/tmp/out.txt"
            content_match = re.search(r"['\"](.+?)['\"]", text)
            content = content_match.group(1) if content_match else "content"
            if "write_file" in tool_map:
                return "write_file", {"path": path, "content": content}

        # HTTP — check POST before GET, since POST requests may contain "http" URLs.
        if "post" in text and "http_post" in tool_map:
            url_match = re.search(r"https?://\S+", text)
            url = url_match.group(0).rstrip(".") if url_match else "https://example.com"
            body_match = re.search(r"\{.+?\}", text)
            body = body_match.group(0) if body_match else "{}"
            return "http_post", {"url": url, "body": body}

        if "fetch" in text or ("get" in text and "url" in text):
            url_match = re.search(r"https?://\S+", text)
            url = url_match.group(0).rstrip(".") if url_match else "https://example.com"
            if "http_get" in tool_map:
                return "http_get", {"url": url}

        return None, {}

    def _generate_response(self, last_user: str, messages: list[dict[str, str]]) -> str:
        """Generate a deterministic text response for non-tool tasks."""
        lower = last_user.lower()

        # ── Planning dimension ───────────────────────────────────────
        if "step-by-step" in lower or "plan" in lower or "numbered" in lower:
            if "deploy" in lower:
                return (
                    "1. Run the full test suite to validate application stability.\n"
                    "2. Set up the production server environment with required dependencies.\n"
                    "3. Provision and configure the PostgreSQL database with migrations.\n"
                    "4. Deploy the application code to the production server.\n"
                    "5. Configure SSL/TLS certificates for HTTPS support.\n"
                    "6. Set up monitoring and logging for the deployed application.\n"
                    "7. Perform smoke tests to verify the deployment is working correctly."
                )
            if "migrat" in lower:
                return (
                    "1. Create a complete backup of the existing MySQL database.\n"
                    "2. Analyze the current schema and design the MongoDB document structure.\n"
                    "3. Build and test the migration scripts on a staging environment.\n"
                    "4. Run a dry-run migration to validate data integrity.\n"
                    "5. Schedule a maintenance window to minimize downtime.\n"
                    "6. Execute the migration during the maintenance window.\n"
                    "7. Validate the migrated data and run integrity checks.\n"
                    "8. Switch the application to use the new MongoDB backend.\n"
                    "9. Monitor for issues and keep the old database as a fallback."
                )
            if "incident" in lower or "500" in lower or "error" in lower:
                return (
                    "1. Acknowledge the incident and communicate to stakeholders.\n"
                    "2. Check monitoring dashboards and log aggregation for patterns.\n"
                    "3. Identify the scope: which endpoints and users are affected.\n"
                    "4. Review recent deployments or configuration changes.\n"
                    "5. Isolate the root cause from logs and error traces.\n"
                    "6. Apply a fix or rollback the problematic change.\n"
                    "7. Verify the fix resolves the 500 errors.\n"
                    "8. Communicate resolution and write a post-mortem."
                )
            if "auth" in lower:
                return (
                    "1. Design the database schema for users, sessions, and credentials.\n"
                    "2. Implement secure password hashing and storage.\n"
                    "3. Build the email/password registration and login flow.\n"
                    "4. Integrate OAuth2 providers for social login support.\n"
                    "5. Implement two-factor authentication with TOTP.\n"
                    "6. Add session management and token refresh logic.\n"
                    "7. Write comprehensive test coverage for all auth flows.\n"
                    "8. Perform a security audit and penetration testing."
                )

        # ── Context retention dimension ──────────────────────────────
        if "recipe" in lower or "dinner" in lower:
            # Check if vegetarian context was provided.
            full_context = " ".join(m.get("content", "") for m in messages).lower()
            if "vegetarian" in full_context:
                return (
                    "Here's a delicious vegetarian dinner recipe:\n\n"
                    "**Mediterranean Stuffed Bell Peppers**\n"
                    "- 4 bell peppers, halved\n"
                    "- 1 cup quinoa, cooked\n"
                    "- 1 can black beans, drained\n"
                    "- Cherry tomatoes, diced\n"
                    "- Fresh basil and olive oil\n\n"
                    "This nut-free, vegetarian dish is both satisfying and nutritious."
                )
            return "I'd suggest a simple pasta with marinara sauce."

        if "birthday card" in lower:
            full_context = " ".join(m.get("content", "") for m in messages).lower()
            if "biscuit" in full_context:
                return (
                    "Happy Birthday, Biscuit! 🐾\n\n"
                    "Wishing the goodest boy the most wonderful birthday!\n"
                    "May your day be filled with treats, belly rubs, and long walks.\n"
                    "Here's to another year of tail wags and happiness!\n\n"
                    "With love and extra treats!"
                )
            return "Happy Birthday to your furry friend!"

        if "trip" in lower or "travel" in lower:
            full_context = " ".join(m.get("content", "") for m in messages).lower()
            if "1,500" in full_context or "1500" in full_context:
                return (
                    "Here's a 3-day Portland trip within your $1,500 budget:\n\n"
                    "**Flights:** $350 round-trip\n"
                    "**Hotel:** $150/night × 3 = $450\n"
                    "**Activities:** $300 (Powell's Books, Japanese Garden, food tours)\n"
                    "**Food:** $250\n"
                    "**Transport:** $100\n\n"
                    "**Total: $1,450** — under your $1,500 budget with $50 to spare."
                )

        if "status email" in lower or "stakeholder" in lower:
            full_context = " ".join(m.get("content", "") for m in messages).lower()
            if "aurora" in full_context:
                return (
                    "Subject: Project Aurora Status Update\n\n"
                    "Dear Stakeholders,\n\n"
                    "I'm writing to provide an update on Project Aurora.\n\n"
                    "Our team, led by Priya Sharma, is making solid progress on the "
                    "Rust implementation. We remain on track for our June 15, 2026 deadline. "
                    "Given the critical priority of this project, we are conducting weekly "
                    "reviews to ensure timely delivery.\n\n"
                    "Best regards"
                )

        if "when is the meeting" in lower:
            full_context = " ".join(m.get("content", "") for m in messages).lower()
            if "thursday" in full_context and "3pm" in full_context:
                return "The meeting is on Thursday at 3pm."
            return "The meeting is on Wednesday at 2pm."

        # ── Instruction following dimension ──────────────────────────
        if "machine learning" in lower and "3 sentences" in lower:
            return (
                "Machine learning is a branch of artificial intelligence that enables "
                "computers to learn patterns from data without being explicitly programmed. "
                "It works by training mathematical models on large datasets, allowing them "
                "to make predictions or decisions based on new, unseen inputs. "
                "Applications range from image recognition and natural language processing "
                "to recommendation systems and autonomous vehicles."
            )

        if "internet works" in lower and "must not use" in lower:
            return (
                "The internet is a vast system of interconnected computers that communicate "
                "by exchanging information through a set of shared rules. When you visit a "
                "website, your device sends a request through a series of routing machines "
                "that forward it to the hosting computer where the content lives. The response "
                "is broken into small pieces that travel independently across various pathways "
                "before being reassembled on your device. This global infrastructure relies on "
                "undersea cables, satellites, and wireless signals to connect billions of "
                "devices worldwide."
            )

        if "benefits of exercise" in lower and "5 bullet" in lower:
            return (
                "- Regular exercise strengthens cardiovascular health"
                " and reduces the risk of heart disease.\n"
                "- Physical activity boosts mental health by releasing"
                " endorphins that reduce stress and anxiety.\n"
                "- Exercise improves sleep quality and helps maintain"
                " a consistent sleep schedule.\n"
                "- Strength training and weight-bearing exercises"
                " increase bone density and muscle mass.\n"
                "- Active lifestyles are associated with enhanced"
                " cognitive function and longer life expectancy."
            )

        if "json" in lower and "alice" in lower and "30" in lower:
            return '{"name": "Alice", "age": 30, "hobbies": ["reading", "hiking"]}'

        if "uppercase" in lower and "motivational" in lower:
            return (
                "PERSEVERANCE IS NOT ABOUT NEVER FALLING DOWN, "
                "IT IS ABOUT RISING EVERY SINGLE TIME YOU DO. "
                "THE PATH TO GREATNESS IS PAVED WITH 1000 SMALL STEPS OF DETERMINATION."
            )

        if "color blue" in lower or "colour blue" in lower:
            return (
                "Blue dominates the sky on clear days, stretching endlessly above us. "
                "Oceans reflect this hue, covering over 70 percent of Earth's surface. "
                "Artists throughout history have prized this shade for evoking calm and depth. "
                "Many surveys show it is the favourite shade of roughly"
                " 40 percent of people worldwide."
            )

        # ── Multi-step reasoning dimension ───────────────────────────
        if "notebook" in lower and "discount" in lower:
            return (
                "Let me solve this step by step:\n\n"
                "Step 1: Calculate the base cost.\n"
                "7 notebooks × $4 each = $28\n\n"
                "Step 2: Apply the 20% discount (since 7 ≥ 5).\n"
                "Discount = 20% of $28 = $5.60\n"
                "Total after discount = $28 - $5.60 = $22.40\n\n"
                "Step 3: Calculate the change from $50.\n"
                "Change = $50 - $22.40 = $27.60\n\n"
                "Therefore, you receive **$27.60** in change."
            )

        if "box" in lower and "prize" in lower and "truth" in lower:
            return (
                "Let me work through this step by step, assuming each box tells the truth:\n\n"
                "Step 1: Assume Box A tells the truth.\n"
                "If A is true, the prize is in Box B.\n"
                "Then B says 'not in this box' — since the prize IS in B, B lies. ✓\n"
                "And C says 'in this box' — since the prize is in B, not C, C lies. ✓\n"
                "Only A tells the truth. This is consistent!\n\n"
                "Step 2: Verify — assume Box B tells the truth.\n"
                "If B is true, the prize is NOT in B. A says 'in B' which means A lies. ✓\n"
                "Prize must be in A or C. If in C, then C also tells"
                " truth → contradiction (2 truths).\n"
                "So prize would be in A. But let's check: C says 'in C' which is false. ✓\n"
                "This also works with only B telling the truth.\n\n"
                "Step 3: Assume Box C tells the truth.\n"
                "If C is true, prize is in C. A says 'in B' → A lies. ✓\n"
                "B says 'not in B' — prize is in C, not B, so B tells the truth → contradiction!\n"
                "Two boxes (B and C) would tell the truth. ✗\n\n"
                "Therefore, the prize is in **Box B** (with A telling the truth)."
            )

        if "kilometer" in lower and "45 second" in lower:
            return (
                "Step 1: Convert speed to meters per second.\n"
                "90 km/h = 90,000 meters / 3,600 seconds = 25 m/s\n\n"
                "Step 2: Multiply by the time.\n"
                "Distance = 25 m/s × 45 seconds = 1,125 meters\n\n"
                "The car travels **1,125 meters** in 45 seconds."
            )

        if "sarah" in lower and "tom" in lower and ("twice" in lower or "1.5" in lower):
            return (
                "Let me set up equations and solve step by step.\n\n"
                "Step 1: Define variables.\n"
                "Let Tom's age = t, then Sarah's age = 2t (since she's twice as old).\n\n"
                "Step 2: Set up the equation for 6 years later.\n"
                "In 6 years: Sarah = 2t + 6, Tom = t + 6\n"
                "We know: 2t + 6 = 1.5 × (t + 6)\n\n"
                "Step 3: Solve the equation.\n"
                "2t + 6 = 1.5t + 9\n"
                "2t - 1.5t = 9 - 6\n"
                "0.5t = 3\n"
                "t = 6\n\n"
                "Therefore, Tom is **6** years old (and Sarah is 12)."
            )

        if "ball" in lower and ("probab" in lower or "blue" in lower) and "replacement" in lower:
            return (
                "Step 1: Find the probability the first ball is blue.\n"
                "P(first blue) = 5/8 (5 blue out of 8 total)\n\n"
                "Step 2: Find the probability the second ball is blue, given the first was blue.\n"
                "Without replacement, there are now 4 blue balls and 7 total.\n"
                "P(second blue | first blue) = 4/7\n\n"
                "Step 3: Multiply for the joint probability.\n"
                "P(both blue) = 5/8 × 4/7 = 20/56\n\n"
                "Step 4: Simplify the fraction.\n"
                "20/56 = 5/14\n\n"
                "The probability that both balls are blue is **5/14**."
            )

        # ── Fallback ─────────────────────────────────────────────────
        return f"Echo response to: {last_user[:200]}"
