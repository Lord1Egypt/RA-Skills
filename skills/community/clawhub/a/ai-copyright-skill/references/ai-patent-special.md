---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '3e4e3e62-27f9-4a74-98e0-4aac48c45855'
  PropagateID: '3e4e3e62-27f9-4a74-98e0-4aac48c45855'
  ReservedCode1: '5fa57445-56ce-458f-834f-78c451c66541'
  ReservedCode2: '5fa57445-56ce-458f-834f-78c451c66541'
---

# AI Patent Drafting Special Guide

## 1. Patentability (§1)

Three elements: Technical Problem (anchored to specific scenario), Technical Means (steps bound to system architecture), Technical Effect (quantifiable).

Domain risk: Generative AI (HIGH - must bind to tech scenario + conditional control), Finance (HIGH - must bind to data processing), AI Alignment (HIGH - must bind to safety), Embodied AI (MED - bind sensor+actuator per step), RL (MED - bind to physical system), RAG (MED - show complete pipeline), AIGC Watermark (MED - bind embedding to model layers).

## 2. Layout Strategy (§2)

Single vs divisional: architecture+training coupled = single; independent innovations = separate filings. 3-part series: (1) Core architecture (2) Training method (3) Inference/deployment. Embodied AI: 2-part (perception-decision + control-execution).

## 3. Paper-to-Patent Mapping (§3)

General 6-type: Problem→Technical Problem, Contribution→Technical Solution, Modules→Implementation Units, Flow→Implementation Flow, Outcome→Expected Effects, Ablation→Dependent Claims.

Domain-specific: 3D Vision (rendering formula→claim step), Gen-AI (noise schedule→claim, condition injection→sub-claim), Embodied (Sim2Real→adaptation step), RL (reward function→computation step), RAG (retrieval strategies→sub-claims), AI Watermark (robustness experiments→verification step), AI4Science (physics constraints→necessary feature).

## 4. Figure Requirements (§4)

13 AI system types each require specific figures: DL inference (architecture+flow), Training (training+augmentation flow), Multimodal (alignment+fusion), Federated (isolation+secure flow), Distillation (teacher-student+accuracy-speed), 3D Vision (capture+reconstruction+rendering), 3DGS/NeRF (representation+rendering+density control), Gen-AI (diffusion+injection+denoising), Embodied (loop+sensor+action space), RAG (retrieval-generation+index), Watermark (embed+extract flow), RL (interaction+policy flow), Agent (tool chain+memory).

## 5. Desensitization (§5)

General 6 types: dataset name→"preset dataset", parameter count→"preset-scale model", hardware→"graphics processor", training duration→"preset period", framework→"DL framework", API→"remote interface".

Industry 14 items: hospital/road/factory/finance/scene/robot/drug/place specifics all replaced with "preset [type]" while retaining category description.

3DGS/NeRF 4 items: Gaussian count→"preset-density 3D Gaussian", SFM library→"sparse reconstruction tool", rendering engine→"real-time rendering engine", sampling params→"preset sampling precision".

## 6. CPC Classification (§6)

AI Core: G06N 3/02-3/10, 3/08, 3/004, G06N 5/00-5/04. Perception: G06V 10-82, 20-80, G06T 7/00-7/70, 11/00, 13-15/00, 1/00, G10L 15-25/00, G01S 13/00. Language: G06F 40/00-58, 16/00. Decision: G05B 19/00, B25J 9/00, B60W 30/00. Safety: G06F 21/00, 21/60, H04L 9/00. Industry: G06Q 10-50/00, A61B 5/00, G16B 40/00, G16C 20/00, G06F 30/00.

## 7. Domain Quick Reference (§7)

Perception→hook: feature extraction improvement→structure: Acquire→Extract→Fuse→Output→metrics: mAP/IoU/PSNR/SSIM. Cognitive→hook: tech-scenario-bound semantics→Encode→Align→Reason→Decode→BLEU/ROUGE. Generative→hook: conditional control means→Condition→Inject→Denoise→Decode→FID/CLIP-Score. Decision→hook: physical loop→Perceive→Plan→Execute→Feedback→success rate. Engineering→hook: training/deployment optimization→Configure→Compute→Optimize→Validate→throughput/accuracy. Safety→hook: safety mechanism binding→Detect/Embed→Compute→Verify→Respond→detection rate/robustness. Industry→hook: domain-specific problem→Data→AI Process→Output→industry KPIs.

> AI生成