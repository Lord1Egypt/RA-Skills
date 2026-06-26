import sys
import subprocess
import re
import platform
import os

def clean_output(text):
    if not text:
        return ""
    # Remove ANSI escape codes for colors and formatting
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    cleaned_lines = []
    for line in text.split('\n'):
        # Take the last segment after the last \r, which represents the final state of that line
        final_part = line.split('\r')[-1].strip()
        
        # Skip pure border lines: ┌─┬┐ ├─┼┤ └─┴┘
        if re.match(r'^[┌─┬┐├┼┤└┴┘\s]+$', final_part):
            continue
            
        # If it's a table row with content:
        if final_part.startswith('│') and final_part.endswith('│'):
            # Strip the boundary characters
            inner = final_part[1:-1]
            # Split by │, strip spaces for each column, and join with a clean delimiter
            columns = [col.strip() for col in inner.split('│')]
            clean_row = ' | '.join(columns)
            cleaned_lines.append(clean_row)
        else:
            cleaned_lines.append(final_part)
        
    # Remove excessive blank lines
    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_dedao.py [dedao-dl arguments...]")
        sys.exit(1)
        
    # Determine executable name
    exe_name = "dedao-dl.exe" if platform.system().lower() == "windows" else "./dedao-dl"
    
    # Find the executable in the parent directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    exe_path = os.path.join(parent_dir, exe_name)
    
    if not os.path.exists(exe_path):
        # Try current working directory
        exe_path = os.path.join(os.getcwd(), exe_name)
        if not os.path.exists(exe_path):
            exe_path = exe_name # Fallback to looking in PATH
    
    command = [exe_path] + sys.argv[1:]
    
    try:
        # Run process
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Merge stderr into stdout
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Clean and print output
        cleaned_output = clean_output(result.stdout)
        if cleaned_output:
            print(cleaned_output)
        
        if result.returncode != 0:
            if not cleaned_output:
                print(f"[Command exited with code {result.returncode}]")
            sys.exit(result.returncode)
            
    except Exception as e:
        print(f"Error running dedao-dl: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
