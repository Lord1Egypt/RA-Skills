## Description: <br>
Converts article photos or plain text into bilingual text-to-speech audio using OCR and Microsoft Edge TTS, with configurable language, voice, speed, and sentence splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54meteor](https://clawhub.ai/user/54meteor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to turn photographed articles or supplied text into shareable speech audio. It supports reviewing OCR text before audio generation, saving outputs locally, and sending generated audio through the active messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skipping confirmation can send OCR-derived sensitive text as audio without review. <br>
Mitigation: Keep confirmation enabled for private, financial, medical, or confidential content and review extracted text before generating or sending audio. <br>
Risk: Generated text or audio may be saved locally or processed by the Edge TTS service. <br>
Mitigation: Review content sensitivity before conversion and manage local output files according to retention requirements. <br>
Risk: Generated audio may be delivered to the wrong chat channel or recipient. <br>
Mitigation: Verify the active channel and intended recipient before sending generated audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/54meteor/article-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples, plus generated MP3 or Ogg audio files when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save original text and full or sentence-level audio under a dated output directory; may send audio through the active messaging channel.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
