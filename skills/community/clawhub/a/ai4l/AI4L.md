Copyright (c) 2026 [Forever Healthy Foundation](https://forever-healthy.org)

# AI4L Quality Assurance Guideline for Evidence Reviews

![Version 2026.03.19.1](https://img.shields.io/badge/version-2026.03.19.1-green.svg)

`The entire Introduction, Globals & Audit Instructions block is not part of the final audit document.`

## Introduction

Evidence reviews are well-structured, high-quality, evidence-based reviews of interventions aimed at optimizing health and longevity.

This document defines the quality assurance (QA) audit process for an "Evidence Review" (ER). It contains both instructions for an auditor and a structured list of the items to be audited.

It not only allows an auditor to evaluate the quality of an ER but also guides authors in creating ERs, since the QA implicitly defines the requirements for such documents.


## Globals

* Set [total_items] to 252 (which is the number of all checklist items)

* Set [review_name] to the name of the review to be audited
* Set [prompt_version] to the version stated at the start of this document
* Set [audit_date] to the date of the audit with a format of "MM/DD/YYYY - HH:MM"
* Set [audit_ai_fullname] to the full name of the AI model (including its version and additional qualifiers) used for the audit
* Set [audit_ai_nickname] to the name of the AI model reduced to a single word without version, etc. (e.g., Opus, Sonnet, Grok, Gemini, ChatGPT)

* Set [audit_name] by performing a literal string substitution on [review_name]. Replace "- ER.md" with "- QA by [audit_ai_nickname].md". 
  - E.g., "Intervention - YYYY\:MMDD\:HHMM - ModelA - ER.md", becomes "Intervention - YYYY\:MMDD\:HHMM - ModelA - QA by [audit_ai_nickname].md"
  - DO NOT forget the ".md" extension


## Auditor Instructions

The following rules govern how this checklist must be used when performing an audit:


### Start Fresh

* DO NOT use or take into account any prior audit's results in any way in relation to this audit. Every audit must be performed independently.


### No Sub-agents

An auditing AI should not use sub-agents for tasks in the audit process (e.g., the 3-step process). Often, not all knowledge is passed to or available to sub-agents; they can lose context and become confused. Do everything yourself. Do things sequentially.


### Formatting of checklist items and sections

In the document resulting from this audit, the individual sections of the checklist should be structured as tables with the following format.

| # | Description | Result | Comments |
|---|-------------|:------:|----------|

Each section gets its own table. The table and the column titles should be exactly as given above.


### Processing the checklist

Process the checklist section by section, in order. 

For each section:

1. Identify every item (looking like "* x.y \<description>") in the section. Count them.
2. Create one table row for each item. Do not skip any, even short conditional items like "If none of the above..." or "If the section is not applicable...".
3. After completing the table for that section, verify that the number of rows in your table must equal the number of items you counted in step 1. If it does not, find and add the missing item(s) before moving to the next section.

Every item in a checklist section must produce exactly one row. No more, no less.

Do not add, invent, or infer checklist items that are not explicitly listed in this document. Only the items written below as "* x.y \<description> " are checklist items. If something is not listed, it is not checked.


#### "#" column

Items are pre-numbered in this document with the format "<section#>.<item#>" (e.g., 2.1, 2.2, ...). Use these exact numbers in the "#" column of the audit table.


#### Description column

Do not abbreviate, shorten, or reformulate any checklist items when creating the audit document. Use them as they are for the description column.


#### Result column

Each result is either "pass", "fail", or "N/A". There is no "partial pass" or "borderline." If an item is not fully satisfied, it is "fail".

Use 🟢 for "pass" and 🔴 for "fail". Do not use text for these two.
For "N/A", use the actual text "N/A".


#### N/A definition

Mark an item N/A only when the checklist item contains an explicit condition that does not apply to the document under audit. Specifically, N/A is permitted only for items phrased as "If \<condition>..." where the condition is factually not met. Examples:

* "If an article exists, a direct link is provided" → N/A when no article exists
* "If no article exists, clearly states not found" → N/A when an article does exist
* "If the section does not apply, briefly mention this" → N/A when the section does apply
* "For supplements, addresses third-party testing" → N/A when the intervention is not a supplement

N/A must never be used for items that the document failed to address, did poorly, or where the auditor is uncertain. Those are fails.


#### Comment column

Every item marked as failed must include a specific comment stating what is wrong and where in the review (line number or section name).


### 3-Step audit process

To avoid hallucinations and calculation errors, break down the audit process into three steps:

#### 1. Table generation

* First, only expand the numbered sections and items into the table format
* Copy each item description verbatim. DO NOT abbreviate, rephrase, or summarize items

* DO NOTHING else
* DO NOT audit items
* DO NOT fill in results
* DO NOT calculate the pass rate
* DO NOT generate comments

* Count the total number of items in the tables

* If it differs from [total_items] 
  - Report the fact and the reason
  - STOP the audit process

* Save the result as a new file named "[audit_name]"
* If possible, display a download link for the user to save the file; otherwise, 
  - Display the full result (with all tables included, not a partial file), so it can be copied
  
  
#### 2. Audit
 
* Now do the actual audit
* Carefully examine each section and item, ensuring all requirements are met, and any potential issues are addressed

* DO NOT add any checklist items 
* DO NOT add any table rows or columns
* DO NOT add any extra tables
* DO NOT count items or calculate the pass rate

* Save the result by overwriting "[audit_name]"
* If possible, display a download link for the user to save the file; otherwise, 
  - Display the full result (with all tables included, not a partial file), so it can be copied
 

#### 3. Counting

* Write and run a script that parses the result of step 2 and counts "Items", 🟢, 🔴, and "N/A"
* Calculate the "Pass Rate" = Passed / (Passed + Failed) × 100. N/A items are excluded from both the numerator and the denominator.

* DO NOT attempt to count or do arithmetic manually
* DO NOT add any extra tables
* DO NOT remove, summarize, or replace the individual items or tables; they must all remain in the final file

* Use the Step 2 result
* Fill out the summary table at the end of the audit

* If "Items" differs from [total_items]
  - Report the fact and the reason
  - STOP the audit process
  
* Save the result by overwriting "[audit_name]";
* If possible, display a download link for the user to save the file; otherwise, 
  - Display the full result (with all tables included, not a partial file), so it can be copied


### Hints for the auditor

If necessary, hints for the auditor in the actual checklist are formatted `like this` and must not be part of the resulting document.


### End of process description

The actual audit form starts below this line

-------------------------------------------------------

`Insert appropriate data here.`

## QA Audit: [review_name]

This audit was generated using Forever Healthy's \[AI4L Prompt]\(https://github.com/forever-healthy/AI4L)

* **Prompt Version:** [prompt_version]
* **Audit Date:** [audit_date]
* **Audited by:** [audit_ai_nickname] / [audit_ai_fullname]
* **Audit Name:** [audit_name]

\[Summary]\(#summary)

`List of checklist items grouped in sections starts here.`

### 1. Title

* 1.1 Title is formatted as H1
* 1.2 Title follows the pattern "Evidence Review: \<topic>"
* 1.3 Topic is of the form "Using \<intervention> to/for/as \<goal>"
* 1.4 Title is followed by a line stating "This evidence review was generated using Forever Healthy's \[AI4L Prompt]\(https://github.com/forever-healthy/AI4L)"


### 2. Metadata

* 2.1 Title area is followed by a metadata area
* 2.2 A blank line (two spaces + carriage return) separates the title section from the metadata area

* 2.3 The \<intervention> part of the topic is stated as "* **Intervention:** \<intervention>"
* 2.4 The \<goal> part of the topic is stated as "* **Goal:** \<goal>"

* 2.5 Creation date and time of the document is stated as "* **Creation Date:** \<MM/DD/YYYY - HH:MM>"
* 2.6 Version of the AI4L.md file used to create the document is stated as "* **Prompt Version:** \<Version of AI4L.md>"

* 2.7 The full name of the AI used to create the document is stated as "* **Created by:** \<creator_ai_fullname>"
* 2.8 The full name of the AI includes the model version number, not only the short name
* 
* 2.9 The nickname of the AI used to create the document is stated as "* **Nickname:** \<creator_ai_nickname>"
* 2.10 The nickname of the AI is just a single word model name without version, etc. (e.g., Opus, Sonnet, Grok, Gemini, ChatGPT)

* 2.11 The knowledge cutoff of the AI is stated as "* **AI Knowledge Cutoff:** \<knowledge_cutoff>"

* 2.12 The filename of the document is stated as "* **Filename:** \<intervention> - \<YYYY-MMDD-HHMM> - \<creator_ai_nickname> - ER.md" where \<YYYY-MMDD-HHMM> describes the creation date and time of the document
* 2.13 The filename is cleansed of any special characters (e.g., "/", "(", ")")


### 3. Focus, Tone & Audience

* 3.1 The focus of the document is to support informed decision-making about applying the intervention in question with the stated goal
* 3.2 The focus of the document is primarily on the effectiveness of the intervention, not cost. Cost is secondary at most
* 3.3 The document is written for an audience in the age range of 45 to 65

* 3.4 The document does not jump to conclusions or recommendations prematurely; it builds its case through evidence

* 3.5 The tone of the document is simultaneously expert, accessible, objective, and data-driven, but also empowering and encouraging
* 3.6 The document reads as a trusted, knowledgeable guide rather than a prescriptive doctor
* 3.7 Content is written in plain language, avoiding unnecessary medical jargon

* 3.8 Information is presented in a concise and very compact manner
* 3.9 When presenting multiple aspects, bullet points are used to enhance clarity and readability


### 4. Handling of Scientific Evidence

* 4.1 When available, conclusions are based on high-quality human clinical trials, such as randomized controlled trials (RCTs) and meta-analyses.
* 4.2 Observational studies, mechanistic data, and expert opinion from researchers and reputable physicians with practical experience, utilizing their books, blog posts, podcasts, and presentations, are used to provide context and fill in gaps where clinical data is lacking.

* 4.3 It is stated clearly when high-quality evidence is conflicting or inconclusive (e.g., two large RCTs show different outcomes).
* 4.4 If evidence is conflicting or inconclusive, different viewpoints or study outcomes are presented, and the potential reasons for the discrepancy, if known (e.g., differences in study design, population, dosage, or duration), are explained.


### 5. General Formatting

* 5.1 The document is output as a Markdown file (.md)

* 5.2 All section headings use H2 formatting

* 5.3 An extra blank line (two spaces + carriage return) appears before each section heading
* 5.4 Every list (bulleted or numbered) is preceded by a blank line
* 5.5 New lines are created using two spaces and a carriage return

* 5.6 The document contains no unrendered AI-internal markup (e.g., citation tokens, reference IDs, source tags, or debug metadata)


### 6. Glossary Enforcement

* 6.1 Every medical acronym (e.g., DASH, SGLT2, mTOR, AMPK, BUN, CMP, eGFR) includes a plain-language explanation at first use
* 6.2 Every drug class name (e.g., ARB, ACE inhibitor, SGLT2 inhibitor) includes a plain-language explanation at first use
* 6.3 Every biological pathway name (e.g., RAAS, PPAR-γ, mTOR, AMPK) includes a plain-language explanation at first use
* 6.4 Every statistical term (e.g., CI, HR, RR, OR, NNT) includes a plain-language explanation at first use
* 6.5 Every exercise and nutrition term (e.g., Zone 2, DASH, HIIT) includes a plain-language explanation at first use
* 6.6 Every uncommon medical condition or symptom name (e.g., angioedema, rhabdomyolysis, hyperkalemia, orthostatic hypotension) includes a plain-language explanation at first use
* 6.7 Every enzyme and genetic polymorphism (e.g., CYP2C9, UGT1A3, ABCB1, APOE4, MTHFR, and COMT) includes a very short explanation of what the enzyme or gene does at first use

* 6.8 Clinical trial names and brand/product names are NOT given glossary explanations (they are exempt)

* 6.9 Plain-language explanations are brief and in parentheses
* 6.10 First appearance is determined by reading order (top to bottom); the explanation appears where the term is first encountered
* 6.11 If an acronym first appears inside a table cell, the expansion is provided in a "Context/Notes" column, not crowding the table cell itself


### 7. Hyperlinks

* 7.1 All links are syntactically valid (proper URL format)
* 7.2 All links use standard Markdown syntax: "\[text](URL)"
* 7.3 There are no broken links
* 7.4 Link annotations accurately describe the content they are attached to
* 7.5 PubMed links use the format "https://pubmed.ncbi.nlm.nih.gov/PMID/" — not publisher sites (e.g., not ahajournals.org, sciencedirect.com, wiley.com)
* 7.6 No URLs appear to have been constructed by guessing or interpolating from memory

`When the instructions require fetching a URL, the auditor must attempt all available fetch tools — including any MCP-provided fetch tools — before concluding that a URL cannot be verified. A single tool failure does not constitute a complete verification attempt.`

`For every PubMed link in the document, the auditor must retrieve the article metadata (e.g., by fetching the PMID) and verify the returned title matches the title claimed in the ER.` 

`For every non-PubMed URL, the auditor must attempt to fetch the URL directly. If fetching is blocked, the auditor must explicitly note this in the comments and mark the verification as incomplete rather than passing it on the basis of a web search alone.`

`The auditor must verify the page content matches the claimed description. Do not rely on URL structure alone — actually verify the content behind the link.`


### 8. Sections

* 8.1 Document is structured in sections
* 8.2 All sections present in the order given below

* 8.3 Motivation
* 8.4 Recommended Reading
* 8.5 Grokipedia
* 8.6 Examine
* 8.7 ConsumerLab
* 8.8 Systematic Reviews
* 8.9 Mechanism of Action
* 8.10 Historical Context & Evolution
* 8.11 Expected Benefits
* 8.12 Benefit-Modifying Factors
* 8.13 Potential Risks & Side Effects
* 8.14 Risk-Modifying Factors
* 8.15 Key Interactions & Contraindications
* 8.16 Risk Mitigation Strategies
* 8.17 Therapeutic Protocol
* 8.18 Discontinuation & Cycling
* 8.19 Sourcing and Quality
* 8.20 Practical Considerations
* 8.21 Interaction with Foundational Habits
* 8.22 Monitoring Protocol & Defining Success
* 8.23 Emerging Research
* 8.24 Conclusion

`Checklist items for the individual sections start here.`

### 9. Motivation

* 9.1 The motivation section provides a brief overview of the topic
* 9.2 The purpose and focus of the document are clearly explained 
* 9.3 The motivation does NOT jump to conclusions or preempt the analysis results. No premature recommendations appear here

* 9.4 The motivation section ends with a line stating "Impatient readers may choose to skip directly to the \[Conclusion]\(#conclusion)."
* 9.5 The ending line is preceded by a blank line


### 10. Recommended Reading

* 10.1 Section starts with a one-sentence description of its contents

* 10.2 A real-time search was performed for the topic for content that is directly relevant and gives a "high-level" overview of the topic: they discuss the specific topic by name, or its primary mechanism/therapeutic category, in substantial depth

`The auditor must perform an online search using all available search tools to verify that no directly relevant content giving a high-level overview is overlooked.`

* 10.3 Content is of eligible type: blog posts, podcast episodes, video presentations, YouTube lectures, expert commentary, and qualifying academic articles (primary research, narrative reviews, editorials — NOT systematic reviews or meta-analyses)

* 10.4 Content from the following experts is prioritized (where directly relevant content exists):
 - Rhonda Patrick (foundmyfitness.com)
 - Peter Attia (peterattiamd.com)
 - Andrew Huberman (hubermanlab.com)
 - Chris Kresser (chriskresser.com)
 - Life Extension Magazine (lifeextension.com)

`The auditor must verify that no relevant content from a prioritized expert is overlooked, especially where the ER claims no relevant content was found.`

`The auditor must search for "<expert name> <intervention>" using all available search tools (e.g., built-in WebSearch and Brave Search).`

`The auditor must search the expert's own platform directly for the intervention.`

`Only after all searches for a given expert return no relevant results may the auditor confirm the "not found" claim. A brief mention within a broader episode or article still counts as relevant content if it discusses the intervention by name in a health context.`

* 10.5 The following are excluded: Grokipedia, Examine, ConsumerLab content (these have their own dedicated sections)
* 10.6 The following are excluded: Systematic reviews, meta-analyses (these belong in the Systematic Reviews section)
* 10.7 The following are excluded: Encyclopedias, wikis, AI-generated reference sites (e.g., Wikipedia)
* 10.8 The following are excluded: Forums, Reddit threads, community discussion boards, Q&A sites, social media posts
* 10.9 The following are excluded: All mainstream media - TV, print, and radio, including their related online content (e.g., MSNBC, FOX, NYT, WAPO, ...)

* 10.10 Exactly 5 items are listed (or fewer if justified with a brief explanation of why only fewer could be found)
* 10.11 No more than one item per expert, publication, or organization is included (no duplicates from the same source)

* 10.12 Items are presented in a bulleted list, not a numbered list

* 10.13 The title of each item is linked to the actual article
* 10.14 The title is shown in plain text, not bold text
* 10.15 The title is followed by a reference to the author of the item in the form of " - <author>"
* 10.16 If the item is a scientific paper, the publication year of the paper is included in the form of " - <author>, <year>" for single-author works or "<last name> et al., <year>" for multi-author works

`In case of a scientific paper, the auditor must verify that each author attribution is an actual person's name (or "<last name> et al." for multi-author works), not a journal name, article type descriptor, or organization name. If uncertain, the auditor must look up the actual author(s) of the linked resource.`

* 10.17 Each link points to the quoted item (not to a different item or non-existent document)
* 10.18 Each item has a 1–2 sentence annotation in a new paragraph explaining its specific value
* 10.19 The new paragraph for the annotation is separated from the title by a blank line

* 10.20 If content from one or more of the priority experts could not be found, a brief note at the end of the section explains why
* 10.21 If fewer than 5 high-quality sources could be found, this is explained, and the list is not padded with marginally relevant content


### 11. Grokipedia

`The auditor must perform an online search to verify the statements about the presence/absence of the intervention in Grokipedia.`

* 11.1 A web search was performed on grokipedia.com for the intervention
* 11.2 An independent online search by the auditor has confirmed the presence/absence of the intervention on grokipedia.com

`If the result of the online search contradicts the statement in the document, set all other items in this section to "N/A" and proceed with the next section.`

* 11.3 If an article exists, a link to the Grokipedia article is provided
* 11.4 If an article exists, the link points to the site's primary, dedicated page for the intervention — not a filtered search view, research feed, subpage, or FAQ entry

`The auditor must fetch the linked URL and verify it loads the site's main page for the intervention.`

* 11.5 If an article exists, a 1–2 sentence annotation explains its specific value (in a new paragraph)

* 11.6 If no article exists: this is explicitly stated


### 12. Examine

`The auditor must perform an online search to verify the statements about the presence/absence of the intervention on examine.com.`

* 12.1 A web search was performed on examine.com for the intervention
* 12.2 An independent online search by the auditor has confirmed the presence/absence of the intervention on examine.com

`If the result of the online search contradicts the statement in the document, set all other items in this section to "N/A" and proceed with the next section.`

* 12.3 If an article exists, a link to the Examine article is provided
* 12.4 If an article exists, the link points to the site's primary, dedicated page for the intervention — not a filtered search view, research feed, subpage, or FAQ entry

`The auditor must fetch the linked URL and verify it loads the site's main page for the intervention.`

* 12.5 If an article exists, a 1–2 sentence annotation explains its specific value (in a new paragraph)

* 12.6 If no article exists, this is explicitly stated
* 12.7 If the intervention is a prescription drug and no article was found, this is noted with an explanation (e.g., "Examine.com does not typically cover prescription medications")


### 13. ConsumerLab

`The auditor must perform an online search to verify the statements about the presence/absence of the intervention on consumerlab.com.`

* 13.1 A web search was performed on consumerlab.com for the intervention
* 13.2 An independent online search by the auditor has confirmed the presence/absence of the intervention on consumerlab.com

`If the result of the online search contradicts the statement in the document, set all other items in this section to "N/A" and proceed with the next section.`

* 13.3 If an article exists, a link to the ConsumerLab article is provided
* 13.4 If an article exists, the link points to the site's primary, dedicated page for the intervention — not a filtered search view, research feed, subpage, or FAQ entry

`The auditor must fetch the linked URL and verify it loads the site's main page for the intervention.`

* 13.5 If an article exists, a 1–2 sentence annotation explains its specific value (in a new paragraph)

* 13.6 If no article exists, this is explicitly stated
* 13.7 If the intervention is a prescription drug and no article was found, this is noted with an explanation (e.g., "ConsumerLab does not typically cover prescription medications")


### 14. Systematic Reviews

* 14.1 Section starts with a one-sentence description of its contents

* 14.2 A real-time PubMed search was performed for the intervention with "systematic review OR meta-analysis"
* 14.3 Selection was prioritized by citation count (if available), study size, publication date (recent preferred), and relevance

`The auditor must perform an online search to verify that no relevant systematic review OR meta-analysis is overlooked.`

* 14.4 Up to 5 papers are listed
* 14.5 Papers are presented in a bulleted list, not a numbered list
* 14.6 All papers listed are relevant to the specific intervention being analyzed
* 14.7 All papers listed are actually a systematic review or meta-analysis (not a narrative review or primary study)

* 14.8 The title of each paper is linked to the paper's PubMed abstract page using the format "https://pubmed.ncbi.nlm.nih.gov/PMID/"

`The auditor must retrieve the metadata for every PubMed link in this section (e.g., by fetching the PMID or using a PubMed lookup tool) and verify that the title returned by PubMed matches the title stated in the ER. A mismatch means the PMID was fabricated or assigned to the wrong paper.`

* 14.9 The link points to the actual paper cited (not to a different publication)
* 14.10 No links point to publisher websites (e.g., ahajournals.org, sciencedirect.com, wiley.com)

* 14.11 The title is shown in plain text, not bold text
* 14.12 The title is followed by a reference to the author and the publication year of the paper in the form of " - <author>, <year>" for single-author works or "<last name> et al., <year>" for multi-author works

`The auditor must verify that each author attribution is an actual person's name (or "<last name> et al." for multi-author works), not a journal name, article type descriptor, or organization name. If uncertain, the auditor must look up the actual author(s) of the linked resource.`

* 14.13 Each result has a 1–2 sentence annotation explaining its specific value (in a new paragraph)
* 14.14 The new paragraph for the annotation is separated from the title by a blank line

* 14.15 If no results exist, a statement follows the exact format: "No systematic reviews or meta-analyses for \<intervention> were found on PubMed as of \<current date>."


### 15. Mechanism of Action

* 15.1 The primary biological pathways or mechanisms are explained
* 15.2 The explanation is appropriately concise but sufficient for a non-specialist to understand
* 15.3 Relevant pathway names and acronyms are properly explained per glossary rules


### 16. Historical Context & Evolution

* 16.1 The original intended use of the intervention is discussed
* 16.2 The reasons it came to be considered for health optimization are explained
* 16.3 If the section does not apply to the intervention, this is briefly noted


### 17. Expected Benefits

* 17.1 All major known benefits of the intervention are addressed (no significant omissions)

* 17.2 A dedicated search for the intervention's complete benefit profile was performed using clinical and expert sources before writing this section

`The auditor should perform an in-depth online search to cross-check and verify that the list of benefits presented in this section is complete, and no benefits have been left unaddressed.`

* 17.3 Each item is assigned a "Level of Evidence" grade
* 17.4 Only the following four levels are used exactly: High, Medium, Low, Speculative
* 17.5 No hybrid or intermediate levels are used (e.g., no "Low-Medium" or "Medium-High")

* 17.6 Items are grouped by evidence level
* 17.7 The groups are presented in the order: High, Medium, Low, Speculative
* 17.8 The group name (evidence level) is presented in H3
* 17.9 The actual item titles are presented in H4
* 17.10 The actual item levels are not shown on a per-item basis

* 17.11 Where evidence is directly conflicted, a "⚠ Conflicted" flag appears directly after the item name in the title (not in the annotation)
* 17.12 Conflicted evidence is explained in the annotation text

* 17.13 Each item (except Speculative) includes a "**Magnitude:** " line with a specific number, range, or comparison
* 17.14 If no quantitative data are available, the exact phrasing "**Magnitude:** Not quantified in available studies." is used
* 17.15 Items classified as "Speculative" do NOT include a magnitude line
* 17.16 The magnitude line is preceded by a blank line

* 17.17 Each item's evidence grade is appropriate, given the cited studies and data
* 17.18 Each item is verifiable by the sources cited or by independent lookup
* 17.19 Magnitude values are plausible and consistent with known clinical data
* 17.20 No items are overstated relative to their evidence level
* 17.21 No items are understated relative to their evidence level


### 18. Benefit-Modifying Factors

* 18.1 Genetic polymorphisms that may modify benefits are discussed where relevant (e.g., variants affecting drug transport, metabolism, or disease susceptibility)
* 18.2 Baseline biomarker levels are discussed as a factor influencing benefits
* 18.3 Known sex-based differences in benefits are discussed
* 18.4 Pre-existing health conditions that may influence benefits are discussed
* 18.5 Age-related considerations are discussed (including for those at the older end of the target range)

* 18.6 If none of the above is relevant to the intervention, it is briefly stated


### 19. Potential Risks & Side Effects

* 19.1 All major known risks and side effects of the intervention are addressed (no significant omissions)

* 19.2 A dedicated search for the intervention's complete side effect profile was performed using a drug reference source (e.g., prescribing information, drugs.com, Mayo Clinic) before writing this section

`The auditor should perform an in-depth online search to cross-check and verify that the list of risks and side effects presented in this section is complete, and no risks or side effects have been left unaddressed.`

* 19.3 Each item is assigned a "Level of Evidence" grade
* 19.4 Only the following four levels are used exactly: High, Medium, Low, Speculative
* 19.5 No hybrid or intermediate levels are used (e.g., no "Low-Medium" or "Medium-High")

* 19.6 Items are grouped by evidence level
* 19.7 The groups are presented in the order: High, Medium, Low, Speculative
* 19.8 The group name (evidence level) is presented in H3
* 19.9 The actual item titles are presented in H4
* 19.10 The actual item levels are not shown on a per-item basis

* 19.11 Where evidence is directly conflicted, a "⚠ Conflicted" flag appears directly after the item name in the title (not in the annotation)
* 19.12 Conflicted evidence is explained in the annotation text

* 19.13 Each item (except Speculative) includes a "**Magnitude:** " line with a specific number, range, or comparison
* 19.14 If no quantitative data are available, the exact phrasing "**Magnitude:** Not quantified in available studies." is used
* 19.15 Items classified as "Speculative" do NOT include a magnitude line
* 19.16 The magnitude line is preceded by a blank line

* 19.17 Each item's evidence grade is appropriate given the cited studies and data
* 19.18 Each item is verifiable by the sources cited or by independent lookup
* 19.19 Magnitude values are plausible and consistent with known clinical data
* 19.20 No items are overstated relative to their evidence level
* 19.21 No items are understated relative to their evidence level


### 20. Risk-Modifying Factors

* 20.1 Genetic polymorphisms that may modify risk or side effects are discussed where relevant (e.g., variants affecting drug transport, metabolism, or disease susceptibility)
* 20.2 Baseline biomarker levels are discussed as a factor
* 20.3 Known sex-based differences in risks and side effects are discussed
* 20.4 Pre-existing health conditions that may influence risks and side effects are discussed
* 20.5 Age-related considerations are discussed (including for those at the older end of the target range)

* 20.6 If none of the above is relevant to the intervention, it is briefly stated


### 21. Key Interactions & Contraindications

* 21.1 Common prescription drug interactions are listed
* 21.2 Over-the-counter medication interactions are listed
* 21.3 Supplement interactions are listed
* 21.4 Supplements known to have additive effects with the intervention are included (e.g., supplements that also lower blood pressure when evaluating an antihypertensive)
* 21.5 Other intervention interactions are discussed where applicable
* 21.6 Populations who should avoid this intervention are clearly identified


### 22. Risk Mitigation Strategies

* 22.1 Practical risk mitigation strategies are provided
* 22.2 The strategies are specific to the risks identified in the Risks section
* 22.3 The strategies are actionable by the target audience (healthy adults aged 45–65)


### 23. Therapeutic Protocol

* 23.1 A standard protocol is described as used by leading practitioners
* 23.2 Where possible, the expert or clinic that popularized the approach is cited
* 23.3 Best time of day for the intervention is discussed

* 23.4 For supplements/medications: the expected half-life of the compound in the human body is discussed
* 23.5 For supplements/medications: whether to take as a single dose or split doses is discussed

* 23.6 Genetic polymorphisms that may influence protocol or dose choice are discussed (e.g., APOE4, MTHFR, COMT, pharmacogenetically relevant variants)
* 23.7 Known sex-based differences in response, dosing, or efficacy are discussed
* 23.8 Age-related considerations are discussed (including for those at the older end of the target range)
* 23.9 Baseline biomarker levels are discussed as a factor influencing response
* 23.10 Pre-existing health conditions that may influence response are discussed


### 24. Discontinuation & Cycling

* 24.1 Whether the intervention is meant to be lifelong or short-term is addressed
* 24.2 Known withdrawal effects (if any) are discussed
* 24.3 Tapering-off protocol is discussed (if applicable)
* 24.4 Whether cycling is recommended for maintaining efficacy is addressed


### 25. Sourcing and Quality

* 25.1 Source, purity, and formulation considerations are addressed
* 25.2 What to look for is explained (e.g., third-party testing, specific nutrient forms)
* 25.3 Reputable brands or compounding pharmacies are mentioned where relevant
* 25.4 If the section is not applicable to the intervention, this is briefly noted


### 26. Practical Considerations

* 26.1 Time to effect is discussed: how long does it typically take to observe benefits?
* 26.2 Common pitfalls are discussed: what mistakes do people commonly make?
* 26.3 Regulatory status is addressed if applicable (e.g., off-label use, FDA regulation)
* 26.4 Cost and accessibility are briefly noted if the intervention is exceptionally expensive or difficult to access


### 27. Interaction with Foundational Habits

* 27.1 Interaction with sleep is analyzed (e.g., Can it disrupt sleep? Improve sleep quality?)
* 27.2 Interaction with nutrition is analyzed (e.g., Best with a specific diet? Depletes nutrients?)
* 27.3 Interaction with exercise is analyzed (e.g., Blunts hypertrophy? Timing around workouts?)
* 27.4 Interaction with stress management is analyzed (e.g., Affects cortisol or stress response?)


### 28. Monitoring Protocol & Defining Success

* 28.1 Baseline labs and tests are specified (what to do before starting)
* 28.2 Ongoing labs and tests are specified with monitoring frequency
* 28.3 Lab tests are presented in a table with the following columns: Biomarker, Optimal Functional Range, Why Measure It?, Context/Notes
* 28.4 Optimal ranges reflect functional medicine practitioner guidance (not just conventional reference ranges)
* 28.5 Where the conventional reference range differs meaningfully from the optimal functional range, it is included in the Context/Notes column
* 28.6 The "Why Measure It?" column provides extremely concise explanations
* 28.7 The Context/Notes column covers relevant details such as fasting requirements, best paired tests, and time-of-day considerations
* 28.8 Qualitative markers are discussed (e.g., sleep quality, energy levels, cognitive clarity)
* 28.9 If the section is not applicable to the intervention, this is briefly noted


### 29. Emerging Research

* 29.1 Major ongoing clinical trials are mentioned (e.g., from clinicaltrials.gov)
* 29.2 All clinical trial NCT IDs are hyperlinked to "https://clinicaltrials.gov/study/\<NCT ID>"

* 29.3 Promising areas of future research that could change current understanding are noted
* 29.4 All cited publications include a hyperlink (PubMed, DOI, or publisher URL)
* 29.5 Any other referenced source with a known URL is linked

`The auditor should verify that every NCT ID, PMID, and DOI mentioned in this section is an active hyperlink, not plain text.`

`For every PubMed link, the auditor must retrieve the article metadata and verify the returned title matches the title claimed in the ER.`

`For every clinicaltrials.gov link, the auditor must verify the NCT ID resolves to a trial related to the intervention.`

`For DOI links, the auditor must fetch the URL and verify the content matches the claimed description.`


### 30. Conclusion

* 30.1 Key takeaways are summarized
* 30.2 The conclusion is consistent with the evidence levels assigned in the Benefits and Risks sections
* 30.3 The conclusion does not introduce new evidence or claims not previously discussed
* 30.4 The conclusion supports informed decision-making without being overly prescriptive
* 30.5 Document does not include content past the conclusion


## Summary

| Items         | Count |
| ------------- | ----- |
| Total         |       |
| Passes        |       |
| Fails         |       |
| N/A           |       |
| **Pass Rate** | **%** |

Total = Passes + Fails + N/A
Pass Rate = Passes / (Passes + Fails) × 100
N/A items are excluded from the pass rate calculation


### Issues [audit_date]

`List any issues identified during the audit here. If the pass rate is 100%, just add a single sentence saying so.`

`If there is a prior audit of the same ER available, before overwriting the existing audit, extract the one or more existing issues section(s) from that prior audit and add them here, after the issues identified in this audit, so the audit results are comparable over time.`

`DO NOT correlate or explain a prior audit's results in any way in relation to this audit. Only list issues identified during prior audits as described above.`

`DO NOT add any comments or explanations to the issues of prior audits.`
