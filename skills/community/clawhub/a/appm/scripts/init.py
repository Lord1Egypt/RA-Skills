import os
import sys
import shutil

def init_appm(project_path):
    project_path = os.path.abspath(project_path)
    openclaw_dir = os.path.join(project_path, ".openclaw")
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")

    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    if not os.path.exists(openclaw_dir):
        os.makedirs(openclaw_dir)
        print(f"Created {openclaw_dir}")
    
    templates = ["MISSION.md", "SNAPSHOT.md", "DECISION_LOG.md"]
    for t in templates:
        src = os.path.join(template_dir, t)
        dst = os.path.join(openclaw_dir, t)
        if not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"Copied template: {t}")
        else:
            print(f"Template already exists: {t}")

    print("\nAPPM Project Initialized Successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init.py <project_path>")
        sys.exit(1)
    
    init_appm(sys.argv[1])
