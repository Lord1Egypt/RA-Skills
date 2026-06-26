import subprocess
import os
import uuid

def run(lh_path, rh_path):
    out_dir = os.path.join("output", str(uuid.uuid4()))
    os.makedirs(out_dir, exist_ok=True)

    matlab_script = f"""
    addpath('matlab');
    brain_as_analysis('{lh_path}', '{rh_path}', '{out_dir}');
    exit;
    """

    subprocess.run([
        "matlab", "-batch", matlab_script
    ])

    return {
        "AS_csv": os.path.join(out_dir, "AS_results.csv"),
        "plots": [
            os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith(".png")
        ]
    }