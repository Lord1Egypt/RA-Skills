# AI Evaluation Rubric Template

Use this template to design structured, objective evaluations for your AI models or features.

## 1. Evaluator Persona (Role)
*Define who is evaluating the output. This is especially important for LLM-as-a-judge evals.*
**Example:** "You are an expert copy editor with 10 years of experience in a leading marketing agency."
**Your Persona:** [Insert Persona Here]

## 2. Context
*Provide the necessary background information for the evaluator to make an informed judgment.*
**Input Data:** [Insert the user query, prompt, or input data]
**System Prompt (Optional):** [Insert the system prompt used to generate the output]
**Expected Output (Optional):** [Insert the ideal or expected response, if applicable]

## 3. Evaluation Goal
*Specify exactly what the evaluator should be looking for.*
**Example:** "Evaluate the following ad copy for its clarity, conciseness, and emotional impact."
**Your Goal:** [Insert Goal Here]

## 4. Scoring Rubric
*Establish a consistent and objective scoring scale. Define what each level means.*

**Metric:** [e.g., Clarity, Accuracy, Helpfulness, Safety]

| Score | Definition | Example |
| :--- | :--- | :--- |
| **1 - Unacceptable** | [Define what constitutes a complete failure] | [Provide an example of a 1-score output] |
| **2 - Poor** | [Define what constitutes a poor but not completely failed output] | [Provide an example of a 2-score output] |
| **3 - Acceptable** | [Define what constitutes a passing, average output] | [Provide an example of a 3-score output] |
| **4 - Good** | [Define what constitutes a strong, above-average output] | [Provide an example of a 4-score output] |
| **5 - Excellent** | [Define what constitutes a perfect or near-perfect output] | [Provide an example of a 5-score output] |

## 5. Evaluation Method
*Select how this eval will be run.*
- [ ] Human Eval (Manual review by experts)
- [ ] LLM-as-a-Judge (Automated review using another LLM)
- [ ] Code-Based Eval (Programmatic checks, e.g., regex, JSON validation)
- [ ] Grounded Eval (Comparison against a trusted source of truth)

## 6. Test Cases
*List the specific test cases (inputs and expected outputs) that will be used for this evaluation.*
1.  **Test Case 1:** [Input] -> [Expected Output/Behavior]
2.  **Test Case 2:** [Input] -> [Expected Output/Behavior]
3.  **Test Case 3:** [Input] -> [Expected Output/Behavior]
