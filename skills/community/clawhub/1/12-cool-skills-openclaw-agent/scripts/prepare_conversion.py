import sys
import os

def prepare_file(file_path):
    """Prépare un fichier pour la conversion en ajoutant des numéros de ligne."""
    if not os.path.exists(file_path):
        print(f"Erreur: Le fichier {file_path} n'existe pas.")
        sys.exit(1)
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    prepared_content = []
    for i, line in enumerate(lines, 1):
        prepared_content.append(f"{i:4} | {line}")
    
    output_path = f"{file_path}.prepared"
    with open(output_path, 'w') as f:
        f.writelines(prepared_content)
    
    print(f"Fichier préparé avec succès : {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 prepare_conversion.py <file_path>")
        sys.exit(1)
    
    prepare_file(sys.argv[1])
