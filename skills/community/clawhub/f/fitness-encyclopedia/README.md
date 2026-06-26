# Fitness Encyclopedia 💪

**Personalized training plans, nutrition calculation, strength prediction, joint assessment, and comprehensive fitness knowledge.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Author](https://img.shields.io/badge/author-Emily%20Yang-purple)

---

## ✨ Features

Fitness Encyclopedia provides comprehensive fitness guidance with AI-powered personalization:

1. **Personalized Training Plans** - Custom workout routines for fat loss, muscle gain, or body sculpting
2. **Nutrition Calculation** - Calculate daily calories and macronutrients based on your goals
3. **Strength Prediction** - Estimate your 1RM (one-rep max) from working weight
4. **Training Plan Details** - Gym and home workout plans with exercise instructions
5. **Cardio Calorie Burn** - Calculate calories burned during different cardio activities
6. **Food Nutrition Database** - Look up nutritional information for common foods
7. **Muscle Stretching Guide** - Proper stretching techniques for recovery and flexibility
8. **Fitness Anatomy** - Learn muscle groups and how they work
9. **Joint Movements & Muscles** - Understand which muscles engage in different exercises
10. **Joint Assessment** - Evaluate joint limitations and get modified workout suggestions
11. **Comprehensive Training Advice** - Professional tips for optimal results

---

## 🚀 Installation

### Via ClawHub (Recommended)

```bash
npx clawhub@latest install fitness-encyclopedia
```

### Via npm

```bash
npm install fitness-encyclopedia
```

---

## 📖 Usage

### Automatic Triggering

The skill automatically activates when you mention:
- `fitness`, `workout`, `training`, `gym`, `exercise`
- `weight-loss`, `muscle-gain`, `fat-loss`, `bodybuilding`
- `fitness-plan`, `personal-trainer`

### Getting Started

Simply say "fitness" or any fitness-related question, and you'll see 11 available modules:

```
你好！我是健身大百科，我可以帮助你：

1. 制定个性化训练计划（减脂/增肌/塑形）
2. 计算热量和营养需求
3. 预测最大力量（1RM）
4. 查询训练计划详情（健身房/居家）
5. 了解有氧运动热量消耗
6. 查询食物营养成分
7. 获取肌肉拉伸指南
8. 学习健身解剖知识
9. 了解关节活动与肌肉
10. 评估关节受限状况
11. 获取综合训练建议

请回复数字，告诉我你需要哪个功能，例如：1
```

### Creating a Personalized Plan

When you choose option 1, the AI will collect:

1. **Basic Info** - Gender, height, weight, age, body fat percentage
2. **Fitness Goal** - Fat loss / Muscle gain / Maintenance / Sculpting
3. **Experience Level** - Beginner / Some experience / Intermediate / Advanced
4. **Time Schedule** - Training time, frequency per week, duration per session
5. **Training Conditions** - Gym access, joint limitations
6. **Dietary Preferences** (Optional) - Food preferences or restrictions

The AI then generates a complete, personalized plan with:
- Weekly workout schedule
- Exercise routines with sets and reps
- Daily calorie and macronutrient targets
- Recovery and stretching recommendations
- Joint-friendly modifications (if needed)

---

## 🧮 Example Workflows

### Nutrition Calculation

```
User: I'm 175cm, 80kg, 30 years old, male. I want to lose fat.

AI: Based on your profile:
- Daily calorie target: 2,000 kcal
- Protein: 160g (32%)
- Carbs: 200g (40%)
- Fat: 67g (28%)
```

### Strength Prediction

```
User: I can bench press 80kg for 8 reps. What's my 1RM?

AI: Your estimated 1RM is approximately 100kg.
Recommended working weight for sets of 8-10 reps: 75-85kg
```

### Joint-Limited Training

```
User: I have knee problems. Can I still train legs?

AI: Yes! Here are knee-friendly leg exercises:
1. Glute bridges - Low knee stress
2. Wall sits - Isometric hold
3. Seated leg extensions - Controlled movement
Avoid: Deep squats, lunges, box jumps
```

---

## 🛠️ Technical Details

### Scripts

- `scripts/calculate_nutrition.py` - Calorie and macro calculations
- `scripts/predict_strength.py` - 1RM strength prediction algorithms

### Reference Materials

- `references/training_plans.md` - Detailed workout plans
- `references/food_nutrition.md` - Food nutrition database
- `references/cardio_calories.md` - Cardio calorie burn rates
- `references/muscle_stretching.md` - Stretching techniques
- `references/muscle_anatomy.md` - Muscle group knowledge
- `references/joint_movements.md` - Joint and muscle relationships
- `references/joint_limited_guide.md` - Joint limitation modifications

### Requirements

- Python 3.x
- OpenClaw runtime
- AI model with natural language understanding

---

## 🎯 Who Should Use This?

- **Beginners** - Get started with safe, effective plans
- **Intermediate Lifters** - Optimize your routines and nutrition
- **Advanced Athletes** - Fine-tune strength and recovery
- **People with Injuries** - Joint-friendly modifications included
- **Busy Professionals** - Time-efficient workout plans

---

## 📝 Author

**Emily Yang** <ywxaswd@gmail.com>

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 🔗 Links

- [GitHub Repository](https://github.com/ywxaswd-stack/fitness-encyclopedia)
- [ClawHub Page](https://clawhub.com/ywxaswd-stack/fitness-encyclopedia)
- [OpenClaw Documentation](https://docs.openclaw.ai)

---

## ⭐ Star on GitHub

If you find this skill helpful, please consider giving it a star on GitHub!

---

Made with 💪 by Emily Yang
