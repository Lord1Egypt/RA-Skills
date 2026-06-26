#!/usr/bin/env python3
"""
Validate Excellent AI Employee Skill structure and content
"""
import os
import sys
import yaml

def validate_skill_structure(base_path):
    """Validate that the skill has correct structure"""
    required_files = [
        'SKILL.md',
        'references/memory-patterns.md',
        'references/task-management.md',
        'references/communication-templates.md',
        'references/quality-checklists.md',
        'references/ethical-guidelines.md'
    ]
    
    errors = []
    
    # Check required files exist
    for filename in required_files:
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            errors.append(f"Missing required file: {filepath}")
    
    # Validate SKILL.md frontmatter
    skill_md_path = os.path.join(base_path, 'SKILL.md')
    if os.path.exists(skill_md_path):
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find YAML frontmatter
            if content.startswith('---\n'):
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    yaml_content = content[4:end_marker]
                    frontmatter = yaml.safe_load(yaml_content)
                    
                    # Check required fields
                    if 'name' not in frontmatter:
                        errors.append("SKILL.md missing 'name' in frontmatter")
                    if 'description' not in frontmatter:
                        errors.append("SKILL.md missing 'description' in frontmatter")
                    
                    # Check name matches expected
                    if frontmatter.get('name') != 'excellent-ai-employee':
                        errors.append(f"SKILL.md name should be 'excellent-ai-employee', got '{frontmatter.get('name')}'")
                else:
                    errors.append("SKILL.md missing closing --- for frontmatter")
            else:
                errors.append("SKILL.md missing YAML frontmatter")
        except Exception as e:
            errors.append(f"Error parsing SKILL.md frontmatter: {e}")
    
    return errors

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <skill_directory>")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    errors = validate_skill_structure(skill_dir)
    
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  ❌ {error}")
        sys.exit(1)
    else:
        print("✅ Skill validation passed!")
        print(f"Excellent AI Employee skill at {skill_dir} is valid.")

if __name__ == "__main__":
    main()