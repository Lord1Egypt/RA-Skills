## Description: <br>
Generate bold concert posters, gig flyers, music event banners, band promo art, festival posters, club night flyers, and live show announcement designs. Perfect for indie musicians, DJs, venue promoters, Bandcamp artists, and tour managers who need eye-catching cinematic poster artwork in seconds via the Neta AI image generation API (free trial at neta.art/open). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as musicians, DJs, venue promoters, Bandcamp artists, and tour managers use this skill to generate concert poster and event artwork from a prompt, with optional sizing and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Poster prompts, optional reference image UUIDs, and the user-supplied Neta token are sent to api.talesofai.com. <br>
Mitigation: Avoid confidential prompts or reference images, and prefer a scoped or disposable token. <br>
Risk: Passing the token on the command line can expose it on shared systems. <br>
Mitigation: Use a scoped or disposable token and avoid running the command where process arguments are visible to untrusted users. <br>


## Reference(s): <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/concert-poster-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt and Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
