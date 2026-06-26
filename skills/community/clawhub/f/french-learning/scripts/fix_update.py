import subprocess
import json

TARGET_SHEET_ID = "1Nnwv4DbbUgfiNDiJdgCvnyxH6oPBis_99fm-2voehl4"
TARGET_SHEET_NAME = "Sheet1"

with open("/tmp/french_learning_output_data.json", "r") as f:
    data = json.load(f)

# Use bash to pass the file content directly
cmd_update = f"gog sheets update {TARGET_SHEET_ID} '{TARGET_SHEET_NAME}!A1' --values-json \"$(cat /tmp/french_learning_output_data.json)\" --json --input=USER_ENTERED"
subprocess.run(cmd_update, shell=True)
