#!/usr/bin/env python3
"""Probe COMSOL Semiconductor all available features."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_features')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')

print("=== All available semiconductor feature types ===")
# List known COMSOL semiconductor feature types
known_types = [
    'SemiconductorMaterialModel',
    'MetalContact',
    'SRHRecombination',
    'AugerRecombination',
    'DirectRecombination',
    'TrapAssistedRecombination',
    'Ionization',
    'Doping',
    'DonorDoping',
    'AcceptorDoping',
    'AnalyticDopingProfile',
    'UniformDopingProfile',
    'GaussianDopingProfile',
    'DopingFeature',
    'SemiconductorDoping',
    'DopingModel',
    'ChargeCarrierTransport',
    'Electrostatics',
    'ConductionCurrent',
    'DisplacementCurrent',
    'Insulation',
    'Ground',
    'ElectricPotential',
    'ContactPotential',
    'SurfaceChargeDensity',
    'SpaceChargeRegion',
    'Continuity',
    'Heterojunction',
    'HeterojunctionBoundaryCondition',
    'InterfaceTrapAssistedRecombination',
    'ThermionicEmission',
    'Tunneling',
    'BandToBandTunneling',
    'MobilityModel',
    'Mobility',
    'ConstantMobility',
    'VelocitySaturation',
    'HighFieldSaturation',
    'CarrierGeneration',
    'OpticalGeneration',
    'UserDefinedGeneration',
]

for name in known_types:
    try:
        feat = semi.create(f'test_{name}', name)
        print(f"  {name}: OK")
    except Exception as e:
        err = str(e)
        if '未知特征' in err or 'Unknown' in err or 'not found' in err.lower():
            pass  # Don't print unknowns to keep output clean
        else:
            print(f"  {name}: ERROR - {err[:120]}")

client.clear()
