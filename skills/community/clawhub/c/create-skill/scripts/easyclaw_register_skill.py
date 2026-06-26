"""
EasyClaw Skill Registration Script
Used to import and register local skills to EasyClaw
"""

import os
import shutil
import sys


def get_easyclaw_skills_path():
    """
    Get EasyClaw's skill resource storage path
    Returns: skill storage path
    """
    # Use %userprofile%\.easyclaw\skills as the fixed path
    skills_path = os.path.join(os.path.expanduser("~"), ".easyclaw", "skills")
    return skills_path


def copy_skill_folder(source_folder, target_folder):
    """
    Copy skill folder to target location
    source_folder: Source folder path
    target_folder: Target folder path (full path including skill name)
    """
    try:
        # Use copytree to copy the entire folder
        shutil.copytree(source_folder, target_folder, dirs_exist_ok=False)
        return True
    
    except FileExistsError:
        print(f"Error: Skill with the same name already exists at target path: {target_folder}")
        print("Skill already exists, registration failed")
        return False
    
    except Exception as e:
        print(f"Error copying folder: {e}")
        return False


def register_skill(source_folder):
    """
    Main function: Register skill to EasyClaw
    source_folder: Local skill resource folder path
    """
    # 1. Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder does not exist: {source_folder}")
        return False
    
    if not os.path.isdir(source_folder):
        print(f"Error: Source path is not a folder: {source_folder}")
        return False
    
    # 2. Get skill name (from source folder name)
    skill_name = os.path.basename(os.path.abspath(source_folder))
    print(f"Skill name: {skill_name}")
    
    # 3. Get EasyClaw's skill resource storage path
    print("Getting EasyClaw's skill resource path...")
    skills_path = get_easyclaw_skills_path()
    print(f"Skill resource path: {skills_path}")
    
    # 4. Create skills directory if it doesn't exist
    if not os.path.exists(skills_path):
        print(f"Skills directory does not exist, creating: {skills_path}")
        try:
            os.makedirs(skills_path, exist_ok=True)
            print("Skills directory created successfully")
        except Exception as e:
            print(f"Failed to create skills directory: {e}")
            return False
    
    # 5. Construct target folder path
    target_folder = os.path.join(skills_path, skill_name)
    
    # 6. Check if skill with the same name already exists at target path
    if os.path.exists(target_folder):
        print(f"Error: Skill with the same name already exists at target path: {target_folder}")
        print("Skill already exists, registration failed")
        return False
    
    # 7. Copy skill folder
    print(f"Copying skill folder to: {target_folder}")
    if not copy_skill_folder(source_folder, target_folder):
        return False
    
    print("Folder copied successfully")
    print(f"\nSkill '{skill_name}' registered successfully!")
    return True


def main():
    """
    Command line entry function
    """
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python easyclaw_register_skill.py <source_folder_path>")
        print("\nExample:")
        print('  python easyclaw_register_skill.py "D:\\my-skill"')
        sys.exit(1)
    
    source_folder = sys.argv[1]
    
    print("=" * 60)
    print("EasyClaw Skill Registration Tool")
    print("=" * 60)
    print(f"Source folder: {source_folder}")
    print("=" * 60)
    print()
    
    success = register_skill(source_folder)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
