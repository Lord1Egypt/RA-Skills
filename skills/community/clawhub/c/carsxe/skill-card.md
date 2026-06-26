## Description: <br>
Access CarsXE vehicle data APIs for VIN decoding, license plate lookup, market value, vehicle history, recalls, lien and theft checks, OBD-II decoding, vehicle images, Year/Make/Model lookups, and plate or VIN OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carsxe](https://clawhub.ai/user/carsxe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select CarsXE REST endpoints, prepare authenticated vehicle-data requests, and present vehicle lookup results for users who provide VINs, license plates, make/model details, OBD codes, or image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle identifiers, license plates, mileage, condition details, and image URLs may be sent to CarsXE during lookups. <br>
Mitigation: Use the skill only when the user intends to send that vehicle data to CarsXE, and confirm before history, lien, theft, plate, VIN, or OCR requests. <br>
Risk: The CarsXE API key and full request URLs are sensitive. <br>
Mitigation: Read the key from CARSXE_KEY, avoid exposing it in responses or logs, and treat keyed request URLs as sensitive. <br>
Risk: Vehicle history, lien, theft, recall, and market-value results can influence buying, safety, or ownership decisions. <br>
Mitigation: Present results as CarsXE API output, highlight important findings clearly, and encourage verification with authoritative records when decisions depend on the result. <br>


## Reference(s): <br>
- [CarsXE API Reference](refernces/api-refernce.md) <br>
- [CarsXE API Documentation](https://api.carsxe.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown with API request examples and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CARSXE_KEY for authenticated CarsXE requests and may summarize JSON responses.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
