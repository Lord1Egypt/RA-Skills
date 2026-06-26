# Script 20: Notebook Starter Template

def create_template():
    template = """
# Engineering Analysis Notebook

## Problem Definition

## Inputs

## Calculations

## Results

## Conclusion
"""
    with open("engineering_template.txt", "w") as f:
        f.write(template)

create_template()
print("Template created.")
