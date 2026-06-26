# Script 64: Engineering Report Generator

def create_report(title, results):
    report = f"\n=== {title} ===\n"

    for key, value in results.items():
        report += f"{key}: {value}\n"

    report += "===================="
    return report

data = {
    "Voltage": "230 V",
    "Current": "10 A",
    "Power": "2300 W"
}

print(create_report("Electrical Analysis Report", data))
