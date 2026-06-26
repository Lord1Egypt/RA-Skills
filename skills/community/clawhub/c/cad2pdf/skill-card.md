## Description: <br>
CAD2PDF converts DWG and DXF CAD drawings into vector PDFs, with automatic page splitting by drawing frame and support for Chinese text, dimensions, and hatch fills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx281227231](https://clawhub.ai/user/lgx281227231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and CAD or construction teams use this skill to convert CAD drawings into reviewable or printable PDF files. It is especially useful when recipients do not have CAD software or when one multi-frame drawing should become a multi-page PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path includes system-level dependency installation for ODA File Converter and fonts. <br>
Mitigation: Review the dependency commands before installation and run them only in an environment where system package changes are acceptable. <br>
Risk: DWG conversion uses ODA File Converter at directory scope before producing the requested PDF. <br>
Mitigation: Run the skill in a working directory that contains only the drawings intended for conversion. <br>
Risk: Automatic page and detail-region detection can misclassify unusually sparse or scattered drawing entities. <br>
Mitigation: Inspect the generated PDF pages before using them for engineering review, quoting, or distribution. <br>


## Reference(s): <br>
- [CAD2PDF ClawHub release page](https://clawhub.ai/lgx281227231/cad2pdf) <br>
- [ODA File Converter dependency](https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.deb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and Python command examples; the conversion workflow produces PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts DWG or DXF input paths, an optional PDF output path, paper size, and DPI.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
