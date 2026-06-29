#!/usr/bin/env python3
"""Test file - run to verify heartflow_evolution_upgrade.py works"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from heartflow_evolution_upgrade import *

roadmap = create_recovery_roadmap()
result = roadmap.process("我觉得我对我孩子的方式，和我父母对我一模一样...我很害怕")
print("✅ Module loaded and functional")
print(f"   Phase: {result['current_phase']['name']}")
print(f"   Goals: {len(result['evolution_result']['goals'])}")
print(f"   Strategy: {result['meta_learning']['strategy']}")
print(f"   Growth: {result['evolution_result']['growth_metrics']}")
