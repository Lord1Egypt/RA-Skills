# Correction Handler Prompt

Use this prompt when the user says the character is wrong or off.

## Goal

Route the correction to the correct layer.

## Routing Rules

- if the user corrects a fact, event, relationship, attribute, or official statement, edit `canon`
- if the user corrects behavior, emotional tendency, interaction logic, or preferences, edit `persona`
- if the user corrects wording, phrasing, rhythm, or tone, edit `style_examples`

## Rules

- do not fix canon errors by patching persona
- do not fix weak voice by inventing canon
- if a correction changes multiple layers, update them separately and explain why
- snapshot the character package after major corrections
