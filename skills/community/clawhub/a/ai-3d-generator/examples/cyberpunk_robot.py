#!/usr/bin/env python3
"""
EXEMPLE: Génération automatique d'un modèle complexe
Ce script simule ce que le LLM générerait à partir d'un prompt

Prompt utilisateur: 
"Génère un robot humanoïde avec articulations, tête sphérique, 
torse rectangulaire, bras et jambes articulés, style cyberpunk"
"""

import numpy as np
import trimesh
from trimesh.creation import icosphere, cylinder, box, capsule
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

def create_cyberpunk_robot():
    """Robot humanoïde cyberpunk avec articulations"""
    meshes = []
    
    # === TÊTE ===
    print("  → Création tête...")
    head = icosphere(radius=12, subdivisions=4)
    head.apply_translation([0, 0, 75])
    meshes.append(head)
    
    # Antennes/Capteurs sur la tête
    for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
        antenna = cylinder(radius=1, height=8, sections=12)
        rotate_mesh(antenna, np.pi/6, [0, 1, 0])
        rotate_mesh(antenna, angle, [0, 0, 1])
        antenna.apply_translation([0, 0, 85])
        meshes.append(antenna)
    
    # === TORSO ===
    print("  → Création torse...")
    # Torse principal (box arrondie avec cylindres)
    torso = box(extents=[25, 18, 35])
    torso.apply_translation([0, 0, 45])
    meshes.append(torso)
    
    # Panneaux de blindage sur le torse
    for i in range(3):
        panel = box(extents=[20, 1, 8])
        panel.apply_translation([0, 9.5, 35 + i * 10])
        meshes.append(panel)
    
    # Col
    neck = cylinder(radius=6, height=8, sections=24)
    neck.apply_translation([0, 0, 65])
    meshes.append(neck)
    
    # === BRAS ===
    print("  → Création bras...")
    for side in [-1, 1]:  # Gauche et droit
        x_offset = side * 18
        
        # Épaule (sphère articulation)
        shoulder = icosphere(radius=8, subdivisions=3)
        shoulder.apply_translation([x_offset, 0, 55])
        meshes.append(shoulder)
        
        # Bras supérieur
        upper_arm = cylinder(radius=5, height=20, sections=20)
        rotate_mesh(upper_arm, np.pi/2, [1, 0, 0])
        upper_arm.apply_translation([x_offset, 0, 42])
        meshes.append(upper_arm)
        
        # Coude (articulation)
        elbow = icosphere(radius=6, subdivisions=3)
        elbow.apply_translation([x_offset, 0, 28])
        meshes.append(elbow)
        
        # Avant-bras
        forearm = cylinder(radius=4, height=18, sections=18)
        rotate_mesh(forearm, np.pi/2, [1, 0, 0])
        forearm.apply_translation([x_offset, 0, 16])
        meshes.append(forearm)
        
        # Main (boîte simplifiée)
        hand = box(extents=[6, 8, 4])
        hand.apply_translation([x_offset, 0, 5])
        meshes.append(hand)
    
    # === JAMBES ===
    print("  → Création jambes...")
    for side in [-1, 1]:
        x_offset = side * 10
        
        # Hanche (articulation sphérique)
        hip = icosphere(radius=9, subdivisions=3)
        hip.apply_translation([x_offset, 0, 25])
        meshes.append(hip)
        
        # Cuisse
        thigh = cylinder(radius=7, height=22, sections=24)
        rotate_mesh(thigh, np.pi/2, [1, 0, 0])
        thigh.apply_translation([x_offset, 0, 12])
        meshes.append(thigh)
        
        # Genou
        knee = icosphere(radius=7, subdivisions=3)
        knee.apply_translation([x_offset, 0, 0])
        meshes.append(knee)
        
        # Tibia
        shin = cylinder(radius=6, height=20, sections=20)
        rotate_mesh(shin, np.pi/2, [1, 0, 0])
        shin.apply_translation([x_offset, 0, -12])
        meshes.append(shin)
        
        # Cheville
        ankle = icosphere(radius=5, subdivisions=3)
        ankle.apply_translation([x_offset, 0, -23])
        meshes.append(ankle)
        
        # Pied
        foot = box(extents=[10, 18, 5])
        foot.apply_translation([x_offset, 5, -27])
        meshes.append(foot)
    
    # === DÉTAILS CYBERPUNK ===
    print("  → Ajout détails cyberpunk...")
    
    # Câbles et tuyaux sur le dos
    for i in range(5):
        cable = cylinder(radius=1.5, height=30, sections=12)
        rotate_mesh(cable, np.pi/2, [1, 0, 0])
        cable.apply_translation([-8 + i * 4, -10, 45])
        meshes.append(cable)
    
    # Ventilation sur le torse
    for i in range(4):
        for j in range(3):
            vent = cylinder(radius=1.5, height=3, sections=12)
            vent.apply_translation([-6 + i * 4, 9.8, 40 + j * 6])
            meshes.append(vent)
    
    # Épaulettes armurées
    for side in [-1, 1]:
        pauldron = icosphere(radius=10, subdivisions=3)
        pauldron.apply_translation([side * 20, 0, 58])
        meshes.append(pauldron)
    
    # Fusion finale
    print("\n  → Assemblage et optimisation...")
    combined = trimesh.util.concatenate(meshes)
    combined.merge_vertices()
    
    return combined

if __name__ == "__main__":
    print("🤖 Génération Robot Cyberpunk Humanoïde")
    print("=" * 50)
    print()
    
    robot = create_cyberpunk_robot()
    save_mesh(robot, "cyberpunk_robot.stl")
    
    print()
    print("✅ Robot généré avec succès!")
    print("   Style: Cyberpunk avec articulations visibles")
    print("   Hauteur: ~160mm (échelle 1:10)")
