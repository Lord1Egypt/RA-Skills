## Description: <br>
High-definition generative speech synthesis using Google Cloud Chirp 3 HD voices for realistic, expressive MP3 speech output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarar21](https://clawhub.ai/user/jarar21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn requested text into natural-sounding speech with Google Cloud Chirp 3 HD voices and receive the generated MP3 file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text provided to the skill is sent to Google Cloud for speech generation. <br>
Mitigation: Use the skill only with content approved for Google Cloud processing and with a least-privilege Google Cloud ADC account. <br>
Risk: The skill may install the Google Cloud Text-to-Speech npm dependency locally on first use. <br>
Mitigation: Run first use in a trusted workspace and review dependency installation policies before enabling automatic execution. <br>
Risk: Generated MP3 files are written to the configured workspace or requested output path. <br>
Mitigation: Use explicit output paths and review workspace permissions before generating speech files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jarar21/g-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP3 audio file with a text success or error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, Google Cloud Application Default Credentials, network access to Google Cloud, and local dependency installation on first use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
