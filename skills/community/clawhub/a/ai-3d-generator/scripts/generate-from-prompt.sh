#!/bin/bash
# Génération automatique de modèle 3D à partir d'un prompt
# Usage: generate-from-prompt.sh "description du modèle" [options]

set -e

PROMPT="${1:-}"
OUTPUT_NAME="${2:-generated_model}"
DETAIL_LEVEL="${3:-high}"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 'description du modèle' [nom_fichier] [detail_level]"
    echo "Exemple: $0 'robot humanoïde avec articulations' robot high"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORT_DIR="/home/celluloid/.openclaw/workspace/stl-exports"
TEMP_SCRIPT="/tmp/auto_3d_$(date +%s).py"

echo "🎨 Génération modèle 3D à partir du prompt..."
echo "Prompt: $PROMPT"
echo ""

# Activer le venv Python
source /home/celluloid/.openclaw/workspace/venvs/cad/bin/activate

# Générer le script Python via le LLM (simulation - en vrai, appeler l'API)
cat > "$TEMP_SCRIPT" << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
Modèle 3D généré automatiquement
Description: {{DESCRIPTION}}
"""

import numpy as np
import trimesh
from trimesh.creation import icosphere, cylinder, cone, torus, box, capsule
from trimesh.transformations import rotation_matrix
import os

EXPORT_DIR = "/home/celluloid/.openclaw/workspace/stl-exports"

def save_mesh(mesh, filename):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filepath = os.path.join(EXPORT_DIR, filename)
    mesh.export(filepath)
    print(f"✓ Exporté: {filepath}")
    print(f"  Triangles: {len(mesh.faces):,}")
    print(f"  Volume: {mesh.volume/1000:.1f} cm³")
    return filepath

def rotate_mesh(mesh, angle, axis, point=None):
    if point is None:
        point = [0, 0, 0]
    mat = rotation_matrix(angle, axis, point)
    mesh.apply_transform(mat)
    return mesh

# === MODÈLE PRINCIPAL ===
def create_model():
    meshes = []
    
    # Corps principal
    body = icosphere(radius=15, subdivisions=3)
    meshes.append(body)
    
    # Détails à ajouter selon le prompt
    # [Le LLM remplacerait cette section]
    
    combined = trimesh.util.concatenate(meshes)
    combined.merge_vertices()
    return combined

if __name__ == "__main__":
    print("Génération du modèle...")
    mesh = create_model()
    save_mesh(mesh, "{{OUTPUT_NAME}}.stl")
    print("✅ Terminé!")
PYTHON_SCRIPT

# Remplacer les placeholders
sed -i "s|{{DESCRIPTION}}|$PROMPT|g" "$TEMP_SCRIPT"
sed -i "s|{{OUTPUT_NAME}}|$OUTPUT_NAME|g" "$TEMP_SCRIPT"

echo "🔧 Exécution du script de génération..."
python3 "$TEMP_SCRIPT"

# Nettoyage
rm -f "$TEMP_SCRIPT"

echo ""
echo "✅ Modèle généré avec succès!"
echo "📁 Emplacement: $EXPORT_DIR/${OUTPUT_NAME}.stl"
