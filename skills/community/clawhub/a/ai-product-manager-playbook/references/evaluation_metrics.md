# AI Evaluation and Metrics (Evals)

This framework guides the AI PM in designing and running systematic evaluations to measure the quality, safety, and reliability of AI products.

## When to use this framework
- Testing a new AI model or prompt before deploying it to production.
- Establishing a baseline for model performance.
- Investigating user reports of poor AI output or hallucinations.

## 1. The Holistic Evaluation Framework
Move beyond simple accuracy metrics. Evaluate across three dimensions:
- **Core Performance:** Accuracy, Precision, Recall, F1-Score. Does the model do what it's supposed to do?
- **User Experience:** Latency, Usability, Trust. Is the product fast, easy to use, and perceived as reliable?
- **Safety and Reliability:** Hallucination Rate, Bias & Fairness, Robustness. Does the model generate false information, exhibit bias, or break under edge cases?

## 2. Designing an Effective Eval
An eval is a structured test that measures output against predefined criteria. Use `templates/ai_eval_rubric.md` to define these components:
- **Action:** Define the **Role** (persona of the evaluator).
- **Action:** Provide the **Context** (necessary background information).
- **Action:** Specify the **Goal** (what the evaluator should look for).
- **Action:** Establish a **Scoring Rubric** (consistent, objective scale with clear definitions).

## 3. Types of Evals
Select the appropriate evaluation method based on the stage of development and the required rigor:
- **Human Evals:** The gold standard. Human experts provide nuanced, qualitative feedback. Slow and expensive.
- **LLM-as-a-Judge:** Use another LLM (e.g., GPT-4) to evaluate the output of the primary model. Fast and scalable, but requires careful prompt design.
- **Code-Based Evals:** Programmatic checks to verify specific aspects (e.g., JSON formatting, presence of specific keywords).
- **Grounded Evals:** Compare the output against a trusted source of truth (e.g., a verified knowledge base).

## 4. Implementation Best Practices
- **Use Real-World Data:** Base your evals on actual user queries and production data, not just synthetic test cases.
- **Build a Taxonomy of Failure Modes:** Categorize how the AI fails (e.g., hallucination, context misunderstanding) to prioritize fixes.
- **Make it a Team Sport:** Collaborate with engineers and designers to define and run evals.
