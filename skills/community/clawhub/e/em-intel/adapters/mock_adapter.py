"""Mock adapters that return realistic synthetic data for --dry-run mode."""

import random
from datetime import datetime, timedelta, timezone
from typing import List

from .base import Branch, CodeAdapter, Epic, MergeRequest, Ticket, TicketAdapter

_ENGINEERS = [
    "alice.chen", "bob.kumar", "carol.west", "david.okafor",
    "elena.silva", "frank.zhang", "grace.lee", "hiro.tanaka",
]

_TICKET_PREFIXES = ["EEH", "PLAT", "INFRA"]

_MR_TITLES = [
    "Add retry logic for payment webhook handler",
    "Fix race condition in order processing queue",
    "Upgrade React to v19 with concurrent features",
    "Refactor auth middleware to use JWT rotation",
    "Add Datadog APM tracing to checkout flow",
    "Fix N+1 query in product catalog endpoint",
    "Implement rate limiting for public API",
    "Add integration tests for Stripe webhook",
    "Migrate user preferences to new schema",
    "Fix timezone handling in scheduled reports",
    "Add OpenTelemetry spans to gRPC services",
    "Implement feature flag for new pricing engine",
    "Fix memory leak in WebSocket connection pool",
    "Add Kafka consumer for inventory updates",
    "Refactor CSV export to streaming response",
]

_TICKET_TITLES = [
    "Implement multi-currency support for checkout",
    "Add bulk import for product catalog",
    "Fix duplicate notification emails on order update",
    "Upgrade Node.js to v22 LTS across services",
    "Add health check endpoint for load balancer",
    "Implement soft-delete for customer accounts",
    "Fix pagination bug in search results API",
    "Add webhook retry with exponential backoff",
    "Migrate legacy cron jobs to Kubernetes CronJob",
    "Implement A/B test framework for pricing page",
    "Fix CORS preflight caching for API gateway",
    "Add audit logging for admin actions",
    "Implement GraphQL subscriptions for real-time updates",
    "Fix CSV injection vulnerability in export",
    "Add rate limit headers to API responses",
]

_EPIC_TITLES = [
    "Q1 Platform Reliability Improvements",
    "Checkout Flow Redesign",
    "API v3 Migration",
    "Observability & Monitoring Overhaul",
    "Multi-tenant Architecture Phase 2",
]


def _random_dt(days_ago_max: int, days_ago_min: int = 0) -> datetime:
    """Generate a random timezone-aware datetime within a range."""
    offset = random.uniform(days_ago_min, days_ago_max)
    return datetime.now(timezone.utc) - timedelta(days=offset)


class MockCodeAdapter(CodeAdapter):
    """Returns realistic synthetic MRs and branches for dry-run mode."""

    def get_merge_requests(self, days: int = 30) -> List[MergeRequest]:
        random.seed(42)  # Deterministic output
        mrs: List[MergeRequest] = []
        count = random.randint(12, 20)

        for i in range(count):
            engineer = random.choice(_ENGINEERS)
            prefix = random.choice(_TICKET_PREFIXES)
            ticket_num = random.randint(100, 999)
            created = _random_dt(days)
            is_merged = random.random() < 0.7
            merged_at = created + timedelta(hours=random.uniform(2, 72)) if is_merged else None

            mrs.append(MergeRequest(
                id=str(1000 + i),
                title=random.choice(_MR_TITLES),
                author=engineer,
                source_branch=f"feature/{prefix}-{ticket_num}-{random.choice(['add', 'fix', 'update', 'refactor'])}-widget",
                state="merged" if is_merged else "opened",
                created_at=created,
                merged_at=merged_at,
                additions=random.randint(5, 500),
                deletions=random.randint(2, 200),
                changed_files=random.randint(1, 15),
                url=f"https://gitlab.example.com/team/project/-/merge_requests/{1000 + i}",
            ))
        return mrs

    def get_branches(self, days: int = 30) -> List[Branch]:
        random.seed(43)
        branches: List[Branch] = []
        count = random.randint(8, 14)

        for i in range(count):
            engineer = random.choice(_ENGINEERS)
            prefix = random.choice(_TICKET_PREFIXES)
            ticket_num = random.randint(100, 999)
            last_commit = _random_dt(days)

            branches.append(Branch(
                name=f"feature/{prefix}-{ticket_num}-{random.choice(['add', 'fix', 'update'])}-{random.choice(['widget', 'service', 'endpoint', 'handler'])}",
                author=engineer,
                last_commit_at=last_commit,
                created_at=last_commit - timedelta(days=random.randint(1, 14)),
                last_commit_sha=f"abc{random.randint(1000, 9999)}def",
            ))
        return branches


class MockTicketAdapter(TicketAdapter):
    """Returns realistic synthetic tickets and epics for dry-run mode."""

    def get_tickets(self, project_keys: List[str]) -> List[Ticket]:
        random.seed(44)
        tickets: List[Ticket] = []
        prefix = project_keys[0] if project_keys else "EEH"
        count = random.randint(15, 25)
        statuses = ["To Do", "In Progress", "In Review", "Done", "Blocked"]

        for i in range(count):
            key = f"{prefix}-{100 + i}"
            assignee = random.choice(_ENGINEERS) if random.random() > 0.2 else None
            tickets.append(Ticket(
                key=key,
                title=random.choice(_TICKET_TITLES),
                status=random.choice(statuses),
                url=f"https://jira.example.com/browse/{key}",
                assignee=assignee,
                ticket_type=random.choice(["Story", "Bug", "Task"]),
                priority=random.choice(["High", "Medium", "Low"]),
                updated_at=_random_dt(30),
            ))
        return tickets

    def get_epics(self, project_keys: List[str]) -> List[Epic]:
        random.seed(45)
        epics: List[Epic] = []
        prefix = project_keys[0] if project_keys else "EEH"
        now = datetime.now(timezone.utc)

        for i, title in enumerate(_EPIC_TITLES):
            key = f"{prefix}-{50 + i}"
            updated = _random_dt(45, 0)
            days_since = (now - updated).days
            epics.append(Epic(
                key=key,
                title=title,
                status=random.choice(["In Progress", "To Do", "In Review"]),
                url=f"https://jira.example.com/browse/{key}",
                assignee=random.choice(_ENGINEERS),
                updated_at=updated,
                days_since_update=days_since,
                child_count=random.randint(3, 12),
            ))
        return epics
