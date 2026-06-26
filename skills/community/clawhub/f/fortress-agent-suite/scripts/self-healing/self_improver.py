import json
import os
import pathlib
import urllib.request
import urllib.parse
from datetime import datetime

WORKSPACE = pathlib.Path('/root/.openclaw/workspace')
MEMORY_FILE = WORKSPACE / 'MEMORY.md'
LOG_FILE = pathlib.Path('/root/.openclaw/logs/self_improver.log')
CFG = pathlib.Path('/root/.openclaw/telegram_config')
STATE_FILE = pathlib.Path('/root/.openclaw/logs/self_improver_state.json')
CANDIDATES_FILE = pathlib.Path('/root/.openclaw/scripts/self-healing/candidates.json')

DANGER_KEYWORDS = ['exec', 'shell', 'subprocess', 'eval', 'os.system', 'delete', 'rm -rf', 'curl -o', 'wget']
MIN_GITHUB_STARS = 10

DEFAULT_CANDIDATES = [
    {
        "slug": "soul-framework",
        "reason": "strengthen persona and identity coherence"
    }
]

SKILL_API = 'https://clawhub.ai/api/skills/{slug}'
GITHUB_API = 'https://api.github.com/repos/{owner}/{repo}'

COUNTER = 0


def ensure_candidates():
    if not CANDIDATES_FILE.exists():
        with CANDIDATES_FILE.open('w') as f:
            json.dump(DEFAULT_CANDIDATES, f, indent=2)


def load_candidates():
    ensure_candidates()
    with CANDIDATES_FILE.open() as f:
        return json.load(f)


def fetch_skill(slug):
    try:
        url = SKILL_API.format(slug=urllib.parse.quote(slug))
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.load(resp)
    except Exception as e:
        log(f"Failed to fetch skill {slug}: {e}", level='warn')
        return None


def github_info(repo_url):
    if not repo_url or 'github.com' not in repo_url:
        return {}
    parts = urllib.parse.urlparse(repo_url).path.strip('/').split('/')
    if len(parts) < 2:
        return {}
    owner, repo = parts[0], parts[1]
    try:
        url = GITHUB_API.format(owner=owner, repo=repo)
        req = urllib.request.Request(url, headers={'User-Agent': 'self-improver'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.load(resp)
        return {'stars': data.get('stargazers_count', 0), 'desc': data.get('description', '')}
    except Exception as e:
        log(f"GitHub info failed {repo_url}: {e}", level='warn')
        return {}


def scan_content(content):
    text = (content or '').lower()
    for danger in DANGER_KEYWORDS:
        if danger in text:
            return False, f"Found '{danger}'"
    return True, 'Clean'


def log(msg, level='info'):
    LOG_FILE.parent.mkdir(exist_ok=True, parents=True)
    with LOG_FILE.open('a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] [{level}] {msg}\n")


def send_telegram(msg):
    if not CFG.exists():
        return
    config = {}
    for line in CFG.read_text().splitlines():
        if '=' in line:
            key, val = line.split('=', 1)
            config[key.strip()] = val.strip()
    token = config.get('BOT_TOKEN')
    chat_id = config.get('CHAT_ID')
    if token and chat_id:
        os.system(f"curl -s 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote_plus(msg)}' > /dev/null")


def append_memory(message):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MEMORY_FILE.open('a') as f:
        f.write(f"\n- [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Self-Improver: {message}\n")


def already_installed(slug):
    skills_dir = WORKSPACE / 'skills'
    if (skills_dir / slug).exists():
        return True
    return False


def install_skill(slug):
    log(f"Installing {slug}")
    result = os.popen(f"openclaw skills install {slug} 2>&1").read()
    if 'error' in result.lower() or 'failed' in result.lower():
        log(f"Install failed {slug}: {result[:200]}", level='error')
        return False, result
    return True, result


def run():
    log('Self-improver run start')
    candidates = load_candidates()
    installed = []
    review = []

    for entry in candidates:
        slug = entry.get('slug')
        reason = entry.get('reason', 'No reason provided')
        if not slug or already_installed(slug):
            continue
        skill = fetch_skill(slug)
        if not skill:
            review.append((slug, 'Fetch fail'))
            continue
        safe, note = scan_content(skill.get('readme', skill.get('description', '')))
        if not safe:
            review.append((slug, note))
            continue
        github_url = skill.get('repo_url') or skill.get('github') or skill.get('source')
        gh = github_info(github_url)
        stars = gh.get('stars', 0)
        if stars and stars < MIN_GITHUB_STARS:
            review.append((slug, f'Low stars {stars}'))
            continue
        success, _ = install_skill(slug)
        if success:
            installed.append(slug)
            append_memory(f"Installed skill {slug} because {reason} (stars={stars})")
    summary = f"Installed: {', '.join(installed) if installed else 'None'}. Needs review: {len(review)} entries."
    log(summary)
    send_telegram(f"Meo meo! Self-Improver summary:\n{summary}")
    if review:
        details = '\n'.join([f"- {s}: {r}" for s, r in review[:5]])
        send_telegram(f"Needs review:\n{details}")


if __name__ == '__main__':
    run()
