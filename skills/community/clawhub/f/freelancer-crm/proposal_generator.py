# proposal_generator.py — generates proposals from template
import json
import os
import sys

def generate_proposal(client_name, project_name, project_cost, project_timeline, freelancer_name="Freelancer"):
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(skill_dir, "templates", "proposal_template.txt")
    
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        return f"Error: template not found at {template_path}"

    # Simple placeholder replacement
    proposal = template.replace("{{ client_name }}", client_name)
    proposal = proposal.replace("{{ project_name }}", project_name)
    proposal = proposal.replace("{{ project_cost }}", project_cost)
    proposal = proposal.replace("{{ project_timeline }}", project_timeline)
    proposal = proposal.replace("{{ freelancer_name }}", freelancer_name)
    
    return proposal

if __name__ == "__main__":
    if len(sys.argv) < 5:
        # Default test case
        print(generate_proposal("Sample Client", "Sample Project", "$500", "1 week"))
    else:
        print(generate_proposal(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))

