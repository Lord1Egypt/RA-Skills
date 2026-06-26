## Description: <br>
Collects product details from 1688 product pages, including images, title, pricing, SKU data, shop information, sales data, attributes, and reviews, then saves a local JSON data package and image folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howerlin0329](https://clawhub.ai/user/howerlin0329) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to archive 1688 product detail pages as local product data packages, including product metadata and downloaded images. It is intended for product research, catalog collection, or workflow support where local review of 1688 product information is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens 1688 pages, downloads product images, and writes JSON plus image folders to a local Desktop or chosen output path. <br>
Mitigation: Run it first on a single product URL, confirm the output path, and monitor disk usage for products with many images. <br>
Risk: Saved product, shop, sales, and review data may be subject to platform rules or privacy obligations. <br>
Mitigation: Review applicable 1688 or Alibaba platform terms and any privacy requirements before storing or reusing collected data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/howerlin0329/1688-scraper) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JavaScript and shell command examples; generated agent work product is local JSON plus downloaded image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a JSON data package and an image directory to the Desktop by default, or to a user-specified output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
