## Description: <br>
酒店比价 helps travelers browse China hotel options and compare prices across Feizhu, Tuniu, Tongcheng, Meituan, and RollingGo before booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to browse hotels by city, date, area, landmark, price, or score, then compare a selected hotel's prices across multiple booking platforms. It returns price comparisons, hotel details, warnings about price variance, and booking links for final user verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details such as city, dates, keywords, and selected hotel names are sent through the publisher's cloud proxy. <br>
Mitigation: Install only when that data flow is acceptable for the intended users and avoid entering sensitive travel details. <br>
Risk: Booking links or tie-breaks may favor commission platforms, and hotel prices can change after comparison. <br>
Mitigation: Treat the results as comparison guidance and verify final price, room type, cancellation terms, and fees on the booking platform before purchase. <br>
Risk: Some platforms may timeout or return no data, so fewer than all five sources may appear in a result. <br>
Mitigation: Review which platforms returned prices and rerun the comparison or check missing platforms directly for high-value bookings. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/travel-skills/skills/china-hotel-price-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with hotel listings, price comparisons, warnings, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browse mode returns curated hotel lists; comparison mode returns ranked platform prices and links for a selected hotel.] <br>

## Skill Version(s): <br>
4.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
