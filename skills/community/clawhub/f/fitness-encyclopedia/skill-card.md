## Description: <br>
Fitness Encyclopedia helps agents answer fitness questions, create personalized workout plans, estimate nutrition targets, predict strength, and provide joint-aware training guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emilyyangmm](https://clawhub.ai/user/emilyyangmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure fitness conversations, gather profile details for workout plans, calculate calorie and macronutrient targets, estimate one-rep max strength, and provide general training guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad fitness-related language, which may route more user interactions through it than expected. <br>
Mitigation: Review trigger behavior before deployment and limit activation scope where the host agent supports narrower routing. <br>
Risk: The skill asks for personal body, diet, and injury details. <br>
Mitigation: Collect only the information needed for the current request, avoid unnecessary sensitive health details, and disclose that responses are general fitness guidance. <br>
Risk: Nutrition, injury, joint, and rehabilitation suggestions may be mistaken for medical advice. <br>
Mitigation: Frame outputs as general fitness information and direct users to qualified medical professionals for injury, rehabilitation, diagnosis, or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emilyyangmm/fitness-encyclopedia) <br>
- [Cardio Calories](references/cardio_calories.md) <br>
- [Food Nutrition](references/food_nutrition.md) <br>
- [Joint Limitation Guide](references/joint_limited_guide.md) <br>
- [Joint Movements](references/joint_movements.md) <br>
- [Muscle Anatomy](references/muscle_anatomy.md) <br>
- [Muscle Stretching](references/muscle_stretching.md) <br>
- [Training Plans](references/training_plans.md) <br>
- [User Interaction Guide](references/user_interaction_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text guidance with optional numeric results from bundled calculation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for body metrics, training schedule, diet preferences, and joint limitation details before generating personalized plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
