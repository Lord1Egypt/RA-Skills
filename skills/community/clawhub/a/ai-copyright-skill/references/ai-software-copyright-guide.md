---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '89964cd3-04e2-4421-b3f9-62ac85847a78'
  PropagateID: '89964cd3-04e2-4421-b3f9-62ac85847a78'
  ReservedCode1: '575b12e2-53d3-43a3-ac3a-98ad4b3f9a82'
  ReservedCode2: '575b12e2-53d3-43a3-ac3a-98ad4b3f9a82'
---

# AI Software Copyright Registration Guide

## 1. Project Type Detection (§1)

Decision tree: app.py→AI Service, train.py→Training, inference.py→Inference, render.py/gaussian.py→3D Vision, diffusion.py→Gen-AI, robot.py/vla.py→Embodied, pipeline.py+langchain→Agent, pipeline.py+rag→RAG, package.json→Frontend. Industry detection: can_bus/lidar→Auto driving, defect/inspection→Industry, dicom/pacs→Healthcare, fraud/credit→Finance, molecule/protein→AI4Science, cultural_heritage→Digital content.

## 2. Source Code Priority (§2)

12-level: (1)model.py (2)train.py (3)inference.py [all required] (4)render.py [3D required] (5)dataset.py (6)loss.py (7)generate.py [Gen-AI required] (8)control.py [Embodied required] (9)retriever.py [RAG required] (10)config.yaml [optional]. Desensitization: remove API keys, absolute paths, internal addresses, personal info, hardware models, cloud URLs, DB passwords; retain algorithm comments. <3000 lines: submit all; >3000: front 1500+back 1500 by priority.

## 3. Manual Templates (§3)

3.1 General: Introduction(env+AI capability)→Installation(env+weights+config)→Functions(AI core+data+API+monitoring)→Non-functional→FAQ.

3.2 3D Vision: Capture+Preprocess→3D Reconstruction(AI core: init, optimize, density control)→Render+Visualize→Export→Non-functional→FAQ.

3.3 Gen-AI: Condition Input(text/ref/control)→Generation Engine(AI core: init, encode+inject, denoise, postprocess)→Result Management→Safety Filtering→Non-functional→FAQ.

3.4 Embodied: Perception(sensor+fusion)→Decision(AI core: instruction parse, VLA fuse, action policy)→Execution(param convert, actuator drive, safety check)→Simulation+Teleoperation→Monitor+Logs→Non-functional→FAQ.

All templates: 10-15 pages, ≥6 screenshots with `[Screenshot: feature]` placeholders, target non-technical reviewers, describe HCI even for server programs, declare open-source weights outside scope.

## 4. Common Pitfalls (§4)

(1) "Pure algorithm not copyrightable"→emphasize software not algorithm (2) Open-source mixing→mark self-developed scope (3) Pre-trained weights→declare outside scope (4) Over-technical→avoid jargon for reviewers (5) Missing HCI steps→describe deploy/config/monitor (6) 3D Vision missing interaction→add viewpoint/params/export steps (7) Gen-AI missing safety→add safety filtering section (8) Embodied missing hardware→detail sensor/actuator/safety (9) RAG KB copyright→declare KB outside scope (10) Edge cross-compilation→prioritize inference+optimization code.

> AI生成