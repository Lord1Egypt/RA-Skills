"""Local storage paths, credentials, and tender-name memory."""

import json
import os


def skill_dir():
    """Return the skill package root directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def creds_path():
    """Credential file path fixed inside the skill package."""
    return os.path.join(skill_dir(), "config.json")


def load_creds_file():
    """Read credentials from the skill-local config.json only."""
    try:
        with open(creds_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, ValueError, OSError):
        pass
    return {}


def save_creds_file(data):
    """Write credentials to skill-local config.json with 0600 permissions."""
    path = creds_path()
    directory = os.path.dirname(path)
    try:
        if directory:
            os.makedirs(directory, exist_ok=True)
    except OSError:
        pass
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def default_output_dir():
    """Default output directory next to the installed skill package."""
    return os.path.join(os.path.dirname(skill_dir()), "biaoshu-writer-service-files")


def output_dir():
    """Resolve and create the generated-document output directory."""
    directory = os.environ.get("ZCM_OUTPUT_DIR", "").strip()
    if not directory:
        directory = str(load_creds_file().get("output_dir") or "").strip()
    directory = os.path.expanduser(directory) if directory else default_output_dir()
    os.makedirs(directory, exist_ok=True)
    return directory


def projects_path():
    home = os.environ.get("ZCM_HOME", "").strip() or os.path.join(os.path.expanduser("~"), ".zcm")
    return os.path.join(home, "projects.json")


def _load_projects():
    try:
        with open(projects_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, ValueError, OSError):
        return {}


def remember_tender(tender_filename, project_id=None, job_id=None):
    """Remember tender filename by project_id/job_id for later report naming."""
    if not tender_filename:
        return
    name = os.path.basename(str(tender_filename).rstrip("/"))
    data = _load_projects()
    by_pid = data.setdefault("by_project", {})
    by_job = data.setdefault("by_job", {})
    if project_id is not None:
        by_pid[str(project_id)] = name
    if job_id is not None:
        by_job[str(job_id)] = name
    path = projects_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def recall_tender(project_id=None, job_id=None):
    """Recall tender filename by job_id/project_id, or None when unavailable."""
    data = _load_projects()
    if job_id is not None:
        value = data.get("by_job", {}).get(str(job_id))
        if value:
            return value
    if project_id is not None:
        value = data.get("by_project", {}).get(str(project_id))
        if value:
            return value
    return None

