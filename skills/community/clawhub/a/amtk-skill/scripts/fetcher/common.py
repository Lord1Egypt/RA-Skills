import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"
QUANT_DATA_ROOT = DATA_ROOT / "quant_data"


def load_simple_dotenv(dotenv_path: Path) -> None:
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_project_dotenv() -> None:
    dotenv_path = PROJECT_ROOT / ".env"
    if not dotenv_path.exists():
        return

    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        load_simple_dotenv(dotenv_path)
        return

    load_dotenv(dotenv_path)


def load_dotenv_if_needed(token: str | None) -> None:
    if token or os.getenv("TUSHARE_TOKEN"):
        return

    load_project_dotenv()


def create_tushare_pro(token: str | None = None):
    try:
        import tushare as ts
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "tushare is required to fetch stock data. Run `uv sync` or install "
            "it with `python3 -m pip install tushare`."
        ) from error

    resolved_token = token or os.getenv("TUSHARE_TOKEN")
    if not resolved_token:
        raise RuntimeError(
            "Missing Tushare token. Set TUSHARE_TOKEN in .env or pass --token YOUR_TOKEN."
        )

    ts.set_token(resolved_token)
    return ts.pro_api()


def tushare_request(callable_name: str, request):
    try:
        return request()
    except Exception as error:
        raise RuntimeError(f"Tushare {callable_name} request failed: {error}") from error

