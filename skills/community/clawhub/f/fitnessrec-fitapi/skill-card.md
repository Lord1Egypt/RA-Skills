## Description: <br>
Precise food and exercise data for AI agents, including nutrient-rich food search, branded barcode lookup, recipe data, exercise search, and personalized daily nutrition needs through FitnessRec FitAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emreakkoc](https://clawhub.ai/user/emreakkoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve precise food, recipe, barcode, exercise, and daily nutrition target data from FitnessRec FitAPI instead of relying on model estimates. It supports nutrition lookup, nutrient filtering, meal planning, barcode product lookup, recipe nutrition review, and exercise programming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a FitnessRec FitAPI key and can consume quota or paid API capacity. <br>
Mitigation: Use a dedicated API key where possible and monitor quota or billing usage. <br>
Risk: Food, exercise, barcode, recipe, and optional body-stat details are sent to FitnessRec's API. <br>
Mitigation: Confirm the user wants personalized or potentially sensitive details used before making those requests, and send only the data needed for the task. <br>
Risk: Broad nutrition and exercise triggers can cause network lookups in ordinary conversation. <br>
Mitigation: Confirm intent before using the API when a request may reveal personal diet, health, or body-measurement information. <br>


## Reference(s): <br>
- [FitnessRec FitAPI skill page](https://clawhub.ai/emreakkoc/fitnessrec-fitapi) <br>
- [FitnessRec FitAPI documentation](https://fitapi.fitnessrec.com/api/docs) <br>
- [FitnessRec FitAPI dashboard](https://fitapi.fitnessrec.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or natural-language responses grounded in FitnessRec API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FitnessRec FitAPI key and network access to FitnessRec endpoints.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
