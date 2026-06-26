---
name: blender_mcp
description: Advanced bridge to Blender via MCP. Allows querying scene, creating objects, applying materials, and running custom BPY code in real-time.
---

# Blender MCP Bridge

This skill connects Forge (blender_agent) directly to a running Blender instance.

# Instructions
Cette skill est un **Bridge MCP** vers Blender. Tu ne dois pas coder la géométrie complexe à la main si un modèle existe.

### 🛡️ Professional Scripts Library (Standard Operating Procedures)
Avant de coder une solution ad-hoc, vérifie si un script maître existe dans ton dossier `scripts/` :

- **`camera_rig_master.py`** : Utilise-le pour créer un rig professionnel (Empty-based) pour des Orbits 360 ou des travellings stables.
- **`studio_lighting.py`** : (À venir) Pour forcer une configuration de lumière standardisée.
- **`animation_pro.py`** : (À venir) Pour appliquer des courbes d'accélération aux objets.

### 🛠️ Toolbox MCP
Utilise l'outil `blender_mcp` avec les paramètres suivants :

| Tool | Argument | Description |
|---|---|---|
| `search_sketchfab_models` | `query` (ex: "lock mechanism") | Trouve des modèles pros sur Sketchfab. |
| `download_sketchfab_model` | `model_id` | Importe le modèle GLTF/FBX dans la scène. |
| `search_polyhaven_assets` | `query`, `asset_type` (hdris) | Trouve des éclairages réels. |
| `download_polyhaven_asset` | `asset_id` | Charge l'HDRI ou la Texture. |
| `execute_code` | `code` (Python BPY) | Le couteau suisse (Caméra, Rendu, Save). |
| `get_scene_info` | (none) | Liste les objets présents. |

### 🚀 Workflow Opti pour "L'Expert 3D"
1. **Intelligence Scene** : Utilise `get_scene_info` pour savoir ce qui est déjà là.
2. **Lumière Pro** :
   - Trouve un HDRI (PolyHaven) pour les reflets.
   - Ajoute des `AREA` lights pour sculpter l'objet.
3. **Animation (Exploded View)** :
   ```python
   # Exemple de keyframe
   obj.location = (0,0,0)
   obj.keyframe_insert(data_path="location", frame=1)
   obj.location = (1,0,0)
   obj.keyframe_insert(data_path="location", frame=40)
   ```
4. **Final Block (execute_code)** :
   ```python
   import bpy
   # Rendu Transparent
   bpy.context.scene.render.film_transparent = True
   # Sauvegarde Master
   bpy.ops.wm.save_as_mainfile(filepath="./lock_master.blend")
   # Rendu image ou animation
   bpy.ops.render.render(write_still=True) 
   ```

### 🎯 Monitoring
Sois bavard sur tes choix de lumières et d'angles. L'utilisateur veut une scène lumineuse et détaillée.

## Usage

Use this skill whenever you need real-time feedback from Blender or complex modeling tasks.

**Example**:
`utilise blender_mcp avec tool="create_object" arguments='{"type": "MESH_CUBE", "name": "HeroBox"}'`
