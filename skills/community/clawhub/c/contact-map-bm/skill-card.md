## Description: <br>
Generate an interactive Germany map of Odoo contacts with clickable markers that open the corresponding Odoo record. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernhmueller](https://clawhub.ai/user/bernhmueller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operations users with Odoo access use this skill to generate a local interactive HTML map of contacts in Germany, optionally filtered by city, with map markers linked back to Odoo records. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: Odoo contact details may be exposed to third-party mapping or geocoding services when coordinates are missing. <br>
Mitigation: Use preexisting coordinates or an approved internal geocoder when possible, and run the skill only for approved contact sets. <br>
Risk: The generated HTML map is a persistent local export that can contain customer, employee, or partner data. <br>
Mitigation: Treat the HTML output as sensitive data, store it in an approved location, and delete it when it is no longer needed. <br>
Risk: The skill requires Odoo credentials with access to contact records. <br>
Mitigation: Use a least-privileged Odoo account or API key and avoid committing credentials or local .env files. <br>


## Reference(s): <br>
- [Contact Map Bm on ClawHub](https://clawhub.ai/bernhmueller/contact-map-bm) <br>
- [Publisher profile: bernhmueller](https://clawhub.ai/user/bernhmueller) <br>
- [Nominatim Search API](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, text] <br>
**Output Format:** [Python script execution that writes an interactive HTML map file and prints a completion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Odoo connection settings via ODOO_URL, ODOO_DB, ODOO_USERNAME, and ODOO_PASSWORD or ODOO_API_KEY; may call Nominatim for geocoding when coordinates are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
