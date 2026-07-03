---
name: Education & Training Assistant
slug: education-training
description: 全能教育培训辅助技能。覆盖K12到高等教育全阶段，支持课程设计、智能组卷与自动批改、知识点图谱生成、个性化学习路径规划、学术论文润色与查重辅助、多语言教学支持。内置Bloom分类学框架与全球主流课程大纲标准（IB/AP/A-Level/高考/考研）。
version: 1.0.0
author: ai-gaoqian
tags:
  - education
  - learning
  - teaching
  - exam
  - academic
metadata:
  openclaw:
    requires:
      - python>=3.10
      - nltk
---

# Education & Training Assistant

All-in-one educational support skill covering K12 to higher education, corporate training, and self-directed learning.

## Core Modules

### 1. Curriculum Design
- Syllabus generation aligned with standards (IB, AP, A-Level, 高考, CBSE, Common Core)
- Unit/lesson plan creation with learning objectives (Bloom's Taxonomy)
- Cross-disciplinary integration mapping
- Prerequisite knowledge graph linking
- Time-boxed semester/quarter planning

### 2. Intelligent Assessment
- Auto-generate questions (MCQ, short answer, essay, coding, math proofs)
- Difficulty calibration (Easy/Medium/Hard → Bloom's levels)
- Automated grading with detailed feedback
- Rubric-based essay evaluation
- Plagiarism detection hints and citation verification
- Item Response Theory (IRT) analysis for question quality

### 3. Knowledge Graph & Learning Path
- Subject-specific concept graphs (Math, Physics, CS, Biology, History, etc.)
- Prerequisite chain visualization
- Personalized learning path based on diagnostic assessment
- Knowledge gap identification and targeted remediation
- Spaced repetition scheduling (SM-2 algorithm)

### 4. Academic Writing Support
- Paper structure review (IMRaD)
- Citation formatting (APA 7, MLA 9, Chicago, GB/T 7714)
- Literature review synthesis assistance
- Argument coherence and logical flow analysis
- Journal/conference matching suggestions
- LaTeX formatting and template generation

### 5. Corporate Training
- Employee onboarding curriculum
- Compliance training content generation
- Skills gap analysis and upskilling paths
- Micro-learning module creation (5-10 min)
- Kirkpatrick evaluation framework integration

### 6. Multi-language Teaching
- Bilingual lesson content generation (CN/EN/JP/KR/FR/DE/ES)
- Translation with pedagogical adaptation
- Cultural context notes for language learners
- Pronunciation guides with IPA notation

## Usage Examples

```yaml
# Generate a physics exam
subject: Physics
level: Grade 11
topics: [Mechanics, Thermodynamics]
format: [MCQ, short_answer, numerical]
difficulty_distribution: {easy: 20%, medium: 50%, hard: 30%}
total_questions: 30
time_limit: 90min
language: bilingual_cn_en

# Create learning path
student_profile:
  current_level: Grade 10 Math
  target: AP Calculus BC
  available_hours_per_week: 8
  preferred_style: visual
output: personalized_study_plan.md
```
