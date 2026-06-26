"""
Fleece CLI — agent-friendly companion to the Fleece Streamlit chatbot.

Exposes credit card research tools as shell commands backed by Brave Search.
Designed for use by AI agents (Claude Code, Codex) and humans alike.

BRAVE_API_KEY is optional — commands that don't need live search (mcc, flights,
hotels) work fully offline. Research commands (card, rates, wallet, …) require it.

Exit codes:
  0  success
  1  search / tool error
  2  BRAVE_API_KEY required but not set
"""
import json
import sys
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

app = typer.Typer(
    name="fleece",
    help=(
        "Fleece credit card research CLI — live data via Brave Search.\n\n"
        "BRAVE_API_KEY is optional: mcc, flights, and hotels work offline.\n"
        "Research commands (card, rates, wallet, …) require it."
    ),
    no_args_is_help=True,
)

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _resolve_key(api_key: Optional[str], no_dotenv: bool) -> str:
    """Load env and return the Brave API key (may be empty — checked at use time)."""
    import os
    if not no_dotenv:
        load_dotenv()
    return api_key or os.getenv("BRAVE_API_KEY", "")


def _get_wrapper(key: str, freshness: Optional[str] = None):
    if not key:
        _error_exit(
            "BRAVE_API_KEY is required for live research. "
            "Set it in your environment, add it to .env, or pass --api-key. "
            "Commands mcc, flights, and hotels work without it.",
            code=2,
        )
    from tools.brave_client import build_brave_wrapper
    return build_brave_wrapper(key, freshness=freshness)


def _read_stdin_or_arg(value: str) -> str:
    """If value is '-', read the first line from stdin."""
    if value == "-":
        return sys.stdin.readline().strip()
    return value


def _emit(result: str, as_json: bool, command: str, query: str) -> None:
    if as_json:
        typer.echo(json.dumps({"command": command, "query": query, "result": result, "ok": True, "error": None}))
    else:
        typer.echo(result)


def _error_exit(message: str, code: int = 1) -> None:
    typer.echo(
        json.dumps({"ok": False, "error": message}),
        err=True,
    )
    raise typer.Exit(code=code)


def _run_search(wrapper, query: str, command: str, as_json: bool) -> None:
    from tools.brave_client import search_and_format
    try:
        result = search_and_format(wrapper, query)
        _emit(result, as_json, command, query)
    except Exception as e:
        _error_exit(str(e), code=1)


# ---------------------------------------------------------------------------
# User profile helpers (fleece.db)
# ---------------------------------------------------------------------------

def _load_profile() -> list[dict]:
    import db
    return db.get_cards()


def _profile_card_names() -> list[str]:
    import db
    return db.get_card_names()


# Reusable option annotations
ApiKeyOpt     = Annotated[Optional[str], typer.Option("--api-key", help="Override BRAVE_API_KEY env var.")]
JsonOpt       = Annotated[bool, typer.Option("--json", "-j", help="Emit JSON output (agent-friendly).")]
NoDotenv      = Annotated[bool, typer.Option("--no-dotenv", help="Skip loading .env file.")]
FromProfileOpt = Annotated[bool, typer.Option("--from-profile", "-p", help="Use cards saved in user_cards.json instead of passing names.")]


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

@app.command()
def card(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Full card report — fees, welcome offer, earning rates, credits, benefits, strategy."""
    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)
    query = f'"{name}" credit card annual fee welcome offer earning rates benefits credits 2025'
    _run_search(_get_wrapper(key), query, "card", as_json)


@app.command()
def rates(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    category:  Annotated[Optional[str], typer.Option("--category", "-c", help="Spending category (dining, travel, groceries…)")] = None,
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Earning rates by spend category — points, miles, or cash back per dollar."""
    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)
    cat  = f"{category} " if category else ""
    query = f'"{name}" {cat}earning rates points miles cashback per dollar categories 2025'
    _run_search(_get_wrapper(key), query, "rates", as_json)


@app.command()
def partners(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Transfer partners — airlines and hotels, ratios, and transfer timing."""
    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)
    query = f'"{name}" transfer partners airlines hotels ratio transfer time 2025'
    _run_search(_get_wrapper(key), query, "partners", as_json)


@app.command()
def credits(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Statement credits and perks — amounts, cadence, and enrollment requirements."""
    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)
    query = f'"{name}" statement credits perks benefits complete list how to use 2025'
    _run_search(_get_wrapper(key), query, "credits", as_json)


@app.command()
def news(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Recent changes in the past month — fee increases, benefit cuts, new perks."""
    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)
    query = f'"{name}" credit card changes update news 2025'
    _run_search(_get_wrapper(key, freshness="pm"), query, "news", as_json)


@app.command()
def compare(
    card_a:    Annotated[str, typer.Argument(help="First card name.")],
    card_b:    Annotated[str, typer.Argument(help="Second card name.")],
    aspects:   Annotated[str, typer.Option("--aspects", help="Comma-separated aspects to compare.")] = "fees,rewards,welcome_offer,credits,transfer_partners",
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """Side-by-side card comparison across fees, rewards, credits, and transfer partners."""
    from tools.brave_client import search_and_format
    key     = _resolve_key(api_key, no_dotenv)
    wrapper = _get_wrapper(key)
    asp     = aspects.replace(",", ", ")

    try:
        result_a = search_and_format(wrapper, f'"{card_a}" credit card {asp} 2025')
        result_b = search_and_format(wrapper, f'"{card_b}" credit card {asp} 2025')
        combined = f"## {card_a}\n{result_a}\n\n## {card_b}\n{result_b}"
    except Exception as e:
        _error_exit(str(e), code=1)
        return
    query    = f"{card_a} vs {card_b}"
    _emit(combined, as_json, "compare", query)


@app.command()
def wallet(
    cards:        Annotated[Optional[list[str]], typer.Argument(help="Card names (space-separated). Omit to use saved profile. Use '-' as sole arg to read from stdin.")] = None,
    from_profile: FromProfileOpt = False,
    api_key:      ApiKeyOpt  = None,
    as_json:      JsonOpt    = False,
    no_dotenv:    NoDotenv   = False,
):
    """Portfolio analysis — category coverage map, overlaps, gaps, and next-card suggestions.

    Card names can come from three sources (in priority order):
    1. Arguments passed directly
    2. --from-profile / -p  (reads user_cards.json)
    3. No args + saved profile exists (auto-loads profile)
    """
    from tools.brave_client import search_and_format

    # Resolve card list
    if cards and cards != ["-"]:
        card_list = cards
    elif cards == ["-"]:
        card_list = [line.strip() for line in sys.stdin if line.strip()]
    else:
        # No args passed — fall back to saved profile
        card_list = _profile_card_names()
        if not card_list:
            _error_exit(
                "No cards provided and user_cards.json is empty. "
                "Pass card names as arguments or add cards with: python cli.py cards add \"<name>\"",
                code=1,
            )

    key     = _resolve_key(api_key, no_dotenv)
    wrapper = _get_wrapper(key)
    parts   = []

    try:
        for name in card_list:
            result = search_and_format(wrapper, f'"{name}" earning rates categories benefits 2025', max_results=2)
            parts.append(f"### {name}\n{result}")
    except Exception as e:
        _error_exit(str(e), code=1)

    import db as _db
    profile_ctx = _db.profile_as_context()

    combined = "\n\n".join(parts)
    combined += "\n\nBased on the above, identify:\n"
    combined += "1. Category coverage map\n"
    combined += "2. Overlapping benefits or redundant categories\n"
    combined += "3. Gaps — categories with no bonus multiplier\n"
    combined += "4. Top 1-2 cards that would complement this portfolio"
    if profile_ctx:
        combined += f"\n\nUser profile context: {profile_ctx}"
        combined += "\nTailor the gap analysis and recommendations to this profile."
    _emit(combined, as_json, "wallet", ", ".join(card_list))


@app.command()
def roi(
    name:      Annotated[str, typer.Argument(help="Card name. Use '-' to read from stdin.")],
    travel:    Annotated[float, typer.Option("--travel",  help="Monthly travel spend ($).")] = 0.0,
    dining:    Annotated[float, typer.Option("--dining",  help="Monthly dining spend ($).")] = 0.0,
    other:     Annotated[float, typer.Option("--other",   help="Monthly other spend ($).")] = 0.0,
    api_key:   ApiKeyOpt  = None,
    as_json:   JsonOpt    = False,
    no_dotenv: NoDotenv   = False,
):
    """First-year ROI estimate — welcome bonus + earn + credits minus annual fee."""
    from tools.brave_client import search_and_format
    from tools.credit_card_tools import _guess_cpp
    import db as _db

    name = _read_stdin_or_arg(name)
    key  = _resolve_key(api_key, no_dotenv)

    # Pull spend values from saved profile if not provided on the command line
    p = _db.get_profile()
    if travel == 0.0 and p.get("travel_monthly"):
        travel = float(p["travel_monthly"])
    if dining == 0.0 and p.get("dining_monthly"):
        dining = float(p["dining_monthly"])
    if other  == 0.0 and p.get("other_monthly"):
        other  = float(p["other_monthly"])

    annual_travel = travel * 12
    annual_dining = dining * 12
    annual_other  = other  * 12
    cpp = _guess_cpp(name)

    try:
        research = search_and_format(
            _get_wrapper(key),
            f'"{name}" annual fee welcome bonus points value first year 2025',
        )
        result = (
            f"Annual spend — Travel: ${annual_travel:,.0f} | Dining: ${annual_dining:,.0f} | Other: ${annual_other:,.0f}\n"
            f"Assumed value per point: {cpp}¢\n\n"
            f"Live research:\n{research}\n\n"
            "Calculate net first-year value: welcome bonus value + estimated annual earn + credits - annual fee. Show the math."
        )
    except Exception as e:
        _error_exit(str(e), code=1)
        return

    _emit(result, as_json, "roi", name)


@app.command()
def recommend(
    profile:     Annotated[str, typer.Argument(help="Spending profile description. Use '-' to read from stdin.")],
    preferences: Annotated[Optional[str], typer.Option("--preferences", "-p", help="Extra preferences (e.g. 'no annual fee').")] = None,
    api_key:     ApiKeyOpt  = None,
    as_json:     JsonOpt    = False,
    no_dotenv:   NoDotenv   = False,
):
    """Card recommendations matched to a spending profile and preferences."""
    import db as _db
    profile = _read_stdin_or_arg(profile)
    key     = _resolve_key(api_key, no_dotenv)
    pref    = f"{preferences} " if preferences else ""

    # Enrich with saved profile context if available
    saved_ctx = _db.profile_as_context(cards=_db.get_card_names())
    ctx = f"{saved_ctx} | " if saved_ctx else ""

    query = f"best credit cards {ctx}{profile} {pref}US 2025 site:nerdwallet.com OR site:thepointsguy.com OR site:doctorofcredit.com"
    _run_search(_get_wrapper(key), query, "recommend", as_json)


# ---------------------------------------------------------------------------
# MCC lookup — offline, no API key required
# ---------------------------------------------------------------------------

def _load_mcc_db() -> dict[str, dict]:
    """Load mcc_codes.jsonl bundled with the package. Returns {mcc: record}."""
    import importlib.resources, pathlib
    # Try installed package data first, fall back to local file
    for candidate in [
        pathlib.Path(__file__).parent / "mcc_codes.jsonl",
    ]:
        if candidate.exists():
            data = {}
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    data[str(rec["mcc"]).zfill(4)] = rec
            return data
    _error_exit("mcc_codes.jsonl not found. Re-install fleece-cli.", code=1)


@app.command()
def mcc(
    code:     Annotated[str, typer.Argument(help="4-digit MCC code, e.g. 5812.")],
    wallet:   Annotated[bool, typer.Option("--wallet", "-w", help="Cross-reference with your saved cards.")] = False,
    api_key:  ApiKeyOpt  = None,
    as_json:  JsonOpt    = False,
    no_dotenv: NoDotenv  = False,
):
    """Look up a Merchant Category Code and find the best card in your wallet to use."""
    code = code.strip().zfill(4)
    db = _load_mcc_db()

    if code not in db:
        _error_exit(f"MCC {code} not found in dataset.", code=1)

    rec = db[code]
    category = rec.get("edited_description") or rec.get("combined_description", "Unknown")
    irs_desc = rec.get("irs_description", "")

    if not wallet:
        if as_json:
            typer.echo(json.dumps({"command": "mcc", "mcc": code, "category": category,
                                   "irs_description": irs_desc, "ok": True, "error": None}))
        else:
            typer.echo(f"MCC {code}: {category}")
            if irs_desc and irs_desc != category:
                typer.echo(f"IRS description: {irs_desc}")
        return

    # Wallet mode — look up earning rates for each card in the profile
    card_names = _profile_card_names()
    if not card_names:
        _error_exit("No cards in profile. Add cards with: fleece cards add \"<name>\"", code=1)

    key = _resolve_key(api_key, no_dotenv)
    from tools.brave_client import search_and_format
    wrapper = _get_wrapper(key)

    parts = []
    try:
        for name in card_names:
            result = search_and_format(
                wrapper,
                f'"{name}" credit card earning rate "{category}" OR "{irs_desc}" category multiplier 2025',
                max_results=2,
            )
            parts.append(f"### {name}\n{result}")
    except Exception as e:
        _error_exit(str(e), code=1)

    combined = (
        f"MCC {code}: {category}\n\n"
        + "\n\n".join(parts)
        + f"\n\nBased on the above, which card earns the most at merchants coded as MCC {code} ({category})? "
        "Show the multiplier for each card and pick the winner."
    )
    _emit(combined, as_json, "mcc", code)


# ---------------------------------------------------------------------------
# Redemption — PointsYeah URL generation (no API key required)
# ---------------------------------------------------------------------------

CABINS = ["economy", "premium-economy", "business", "first"]


@app.command()
def flights(
    origin:      Annotated[str, typer.Argument(help="Origin airport code (e.g. JFK).")],
    destination: Annotated[str, typer.Argument(help="Destination airport code (e.g. LAX).")],
    date:        Annotated[str,  typer.Option("--date", help="Departure date (YYYY-MM-DD).")],
    return_date: Annotated[Optional[str], typer.Option("--return", help="Return date (YYYY-MM-DD).")] = None,
    adults:      Annotated[int,  typer.Option("--adults", min=1)] = 1,
    cabin:       Annotated[str,  typer.Option("--cabin", help=f"Cabin class: {', '.join(CABINS)}.")] = "economy",
    open_url:    Annotated[bool, typer.Option("--open", help="Open URL in browser.")] = False,
    as_json:     JsonOpt = False,
):
    """Generate a PointsYeah flight search URL and optionally open it."""
    import webbrowser
    from pointsyeah import FlightsQuery, build_flights_url

    if cabin not in CABINS:
        _error_exit(f"Invalid cabin '{cabin}'. Choose from: {', '.join(CABINS)}")

    q = FlightsQuery(origin=origin, destination=destination, date=date,
                     return_date=return_date, adults=adults, cabin=cabin)
    url = build_flights_url(q)

    if as_json:
        import dataclasses
        typer.echo(json.dumps({"command": "flights", **dataclasses.asdict(q), "url": url, "ok": True, "error": None}))
    else:
        typer.echo(url)

    if open_url:
        webbrowser.open(url)


@app.command()
def hotels(
    location: Annotated[str, typer.Argument(help="City, area, or hotel keyword.")],
    checkin:  Annotated[str, typer.Option("--checkin",  help="Check-in date (YYYY-MM-DD).")],
    checkout: Annotated[str, typer.Option("--checkout", help="Check-out date (YYYY-MM-DD).")],
    guests:   Annotated[int, typer.Option("--guests", min=1)] = 1,
    rooms:    Annotated[int, typer.Option("--rooms",  min=1)] = 1,
    open_url: Annotated[bool, typer.Option("--open", help="Open URL in browser.")] = False,
    as_json:  JsonOpt = False,
):
    """Generate a PointsYeah hotel search URL and optionally open it."""
    import webbrowser
    from pointsyeah import HotelsQuery, build_hotels_url

    q = HotelsQuery(location=location, checkin=checkin, checkout=checkout,
                    guests=guests, rooms=rooms)
    url = build_hotels_url(q)

    if as_json:
        import dataclasses
        typer.echo(json.dumps({"command": "hotels", **dataclasses.asdict(q), "url": url, "ok": True, "error": None}))
    else:
        typer.echo(url)

    if open_url:
        webbrowser.open(url)


# ---------------------------------------------------------------------------
# profile — spending profile management
# ---------------------------------------------------------------------------

profile_app = typer.Typer(name="profile", help="Manage your spending profile — used to personalise research commands.", no_args_is_help=True)
app.add_typer(profile_app)


@profile_app.command("show")
def profile_show(as_json: JsonOpt = False):
    """Show your current spending profile."""
    import db as _db
    p = _db.get_profile()
    if not p:
        typer.echo("No profile set. Run: fleece profile set <field> <value>")
        typer.echo(f"Fields: {', '.join(_db.PROFILE_FIELDS)}")
        return
    if as_json:
        typer.echo(json.dumps({"command": "profile show", "profile": p, "ok": True, "error": None}))
        return
    for key, label in _db.PROFILE_FIELDS.items():
        val = p.get(key, "")
        if val:
            typer.echo(f"  {label:<45} {val}")


@profile_app.command("set")
def profile_set(
    field: Annotated[str, typer.Argument(help=f"Field name. One of: {', '.join(__import__('db').PROFILE_FIELDS)}")],
    value: Annotated[str, typer.Argument(help="Value to set.")],
    as_json: JsonOpt = False,
):
    """Set a profile field."""
    import db as _db
    try:
        _db.set_profile_field(field, value)
    except ValueError as e:
        _error_exit(str(e), code=1)
    if as_json:
        typer.echo(json.dumps({"command": "profile set", "field": field, "value": value, "ok": True, "error": None}))
    else:
        typer.echo(f"Profile updated: {field} = {value}")


@profile_app.command("unset")
def profile_unset(
    field: Annotated[str, typer.Argument(help="Field name to clear.")],
    as_json: JsonOpt = False,
):
    """Clear a single profile field."""
    import db as _db
    _db.clear_profile_field(field)
    if as_json:
        typer.echo(json.dumps({"command": "profile unset", "field": field, "ok": True, "error": None}))
    else:
        typer.echo(f"Cleared: {field}")


@profile_app.command("fields")
def profile_fields():
    """List all available profile fields and their descriptions."""
    import db as _db
    for key, label in _db.PROFILE_FIELDS.items():
        typer.echo(f"  {key:<30} {label}")


# ---------------------------------------------------------------------------
# cards — profile management (read/write user_cards.json)
# ---------------------------------------------------------------------------

cards_app = typer.Typer(name="cards", help="Manage your saved card profile (user_cards.json).", no_args_is_help=True)
app.add_typer(cards_app)


@cards_app.command("list")
def cards_list(
    as_json: JsonOpt = False,
):
    """List all cards saved in your profile."""
    profile = _load_profile()
    if not profile:
        typer.echo("No cards in profile. Add one with: python cli.py cards add \"<card name>\"")
        return
    if as_json:
        typer.echo(json.dumps({"command": "cards list", "cards": profile, "ok": True, "error": None}))
    else:
        for i, card in enumerate(profile, 1):
            fee = card.get("annual_fee", "N/A")
            typer.echo(f"{i}. {card['name']}  (fee: {fee})")


@cards_app.command("add")
def cards_add(
    name:       Annotated[str, typer.Argument(help="Card name to add.")],
    annual_fee: Annotated[str, typer.Option("--fee", help="Annual fee (e.g. $95).")] = "$0",
    as_json:    JsonOpt = False,
):
    """Add a card to your profile."""
    import datetime
    import db
    new_card = {
        "name": name,
        "annual_fee": annual_fee,
        "date_added": datetime.date.today().isoformat(),
    }
    try:
        db.add_card(new_card)
    except ValueError as e:
        _error_exit(str(e), code=1)
    total = len(db.get_card_names())
    if as_json:
        typer.echo(json.dumps({"command": "cards add", "card": new_card, "ok": True, "error": None}))
    else:
        typer.echo(f'Added "{name}" to your profile. ({total} card(s) total)')


@cards_app.command("remove")
def cards_remove(
    name:    Annotated[str, typer.Argument(help="Card name to remove (partial match OK).")],
    as_json: JsonOpt = False,
):
    """Remove a card from your profile."""
    import db
    # Partial match against all names
    all_cards = db.get_cards()
    matches = [c for c in all_cards if name.lower() in c["name"].lower()]
    if not matches:
        _error_exit(f'No card matching "{name}" found in profile.', code=1)
    if len(matches) > 1:
        names = ", ".join(f'"{c["name"]}"' for c in matches)
        _error_exit(f'Ambiguous match — found {names}. Be more specific.', code=1)
    removed = matches[0]
    db.remove_card(removed["name"])
    remaining = len(db.get_card_names())
    if as_json:
        typer.echo(json.dumps({"command": "cards remove", "removed": removed["name"], "ok": True, "error": None}))
    else:
        typer.echo(f'Removed "{removed["name"]}" from your profile. ({remaining} card(s) remaining)')


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
