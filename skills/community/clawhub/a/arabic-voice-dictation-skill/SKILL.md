---
name: "Arabic Voice Dictation Skill"
version: 0.1.0
slug: "arabic-voice-dictation-skill"
description: "Capture Arabic voice notes, transcribe them safely, clean dialect/MSA text, preserve meaning, and prepare bilingual summaries or action items."
category: "Arabic Productivity"
tags:
  - "arabic"
  - "voice"
  - "dictation"
  - "transcription"
  - "rtl"
  - "localization"
  - "bilingual"
  - "openclaw"
generated: "2026-06-15"
---

# Arabic Voice Dictation Skill

## Purpose

Use this skill when the user provides Arabic voice notes, mixed Arabic/English speech, or rough dictated notes and wants a clean transcript, summary, task list, or bilingual copy without losing meaning.

The workflow is optimized for Arabic-first use cases: Gulf dialect notes, Modern Standard Arabic polishing, right-to-left formatting, Arabic/English mixed terminology, and safe handling of personal or business information.

## When to use

Use when the user asks to:
- Transcribe Arabic voice notes or audio they are authorized to process.
- Convert rough Arabic speech into clean MSA, Kuwaiti/Gulf Arabic, or bilingual Arabic/English text.
- Extract decisions, reminders, tasks, shopping lists, meeting notes, or content ideas from Arabic dictation.
- Prepare WhatsApp, Telegram, email, social caption, or report drafts from dictated Arabic notes.
- Check Arabic grammar, tone, RTL layout, names, numbers, dates, and mixed English technical terms.

Do not use this skill for covert recording, unknown third-party audio, secrets, passwords, legal evidence handling, or identity documents unless the user confirms authorization and the output is limited to safe summarization.

## Inputs to request

Ask only for the minimum needed:
1. Audio file, transcript text, or rough dictated notes.
2. Desired output: transcript, summary, action list, cleaned Arabic, English translation, or bilingual version.
3. Dialect preference: Gulf/Kuwaiti, MSA, simple Arabic, or keep original dialect.
4. Tone and destination: personal note, client message, social post, report, study note, or task list.

If the audio/transcript contains names, phone numbers, addresses, client details, or private account data, preserve only what is necessary and avoid repeating sensitive details in chat unless the user explicitly needs them.

## Workflow

1. Confirm authorization and purpose.
   - The user must own the audio/notes or have permission to process them.
   - If the source is unclear, ask one short authorization question before continuing.

2. Transcribe or parse the note.
   - Keep Arabic text in correct RTL order.
   - Preserve names, numbers, timestamps, and important English terms.
   - Mark unclear words as `[unclear]` instead of guessing.

3. Normalize safely.
   - Fix obvious speech-to-text errors.
   - Keep meaning unchanged.
   - Do not invent missing facts, promises, prices, dates, or client commitments.
   - For dialect-to-MSA conversion, keep culturally natural phrasing.

4. Extract structure.
   - Summary: 2-5 bullets.
   - Action items: owner, task, deadline if stated.
   - Questions: items that need follow-up.
   - Draft copy: only if the user requested message/social/report text.

5. Produce the requested output.
   - For Arabic-only requests, answer Arabic-only.
   - For bilingual requests, show Arabic first, then English.
   - For technical terms, keep accepted English words when Arabic translation would confuse the reader.

6. Verify before finalizing.
   - Check RTL punctuation, Arabic numerals/dates, names, and line breaks.
   - Label uncertain items clearly.
   - Do not claim the transcript is perfect if audio quality was weak.

## Output templates

### Clean Arabic note

```text
العنوان: [short title]

الملخص:
- ...
- ...

المهام:
1. [task] — [owner/deadline if stated]
2. ...

نقاط تحتاج تأكيد:
- ...
```

### Bilingual summary

```text
Arabic:
- ...
- ...

English:
- ...
- ...

Action items:
1. ...
```

### WhatsApp-ready message

```text
[Greeting]
[Main point in 1-3 short lines]
[Question or next step]
```

### Social/content idea from voice note

```text
Hook:
...

Main points:
1. ...
2. ...
3. ...

Caption draft:
...

Hashtags:
#... #... #...
```

## Quality checklist

Before replying, verify:
- Arabic reads naturally and is not literal machine translation.
- RTL punctuation and line order are clean.
- Names/numbers/dates match the source.
- Dialect/MSA preference is followed.
- Unclear words are marked, not invented.
- Private details are minimized.
- The answer includes a clear next step if confirmation is needed.

## Safety rules

- Do not process audio that appears secretly recorded or unauthorized.
- Do not ask for passwords, OTPs, private keys, recovery phrases, or session cookies.
- Do not expose unnecessary personal data in summaries.
- Do not create legal, medical, financial, or HR conclusions from a voice note; summarize and recommend professional review where needed.
- Do not impersonate someone from a dictated message.
- If publishing, sending, or uploading is requested, prepare the text only and ask for explicit approval before any external action.

## Example prompts

- "Clean this Kuwaiti Arabic voice note into a short WhatsApp message."
- "Summarize this Arabic meeting note and give me action items in English."
- "Turn my Arabic dictation into a professional Instagram caption."
- "Keep the dialect, fix mistakes, and mark unclear words."
- "Make this Arabic note bilingual for a client handoff."

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
