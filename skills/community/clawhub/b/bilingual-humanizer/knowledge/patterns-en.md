# Knowledge Base: Pattern Dictionary (English)

This document details the 29 specific writing patterns detected in English. Use these definitions to understand the logic behind the flags and how to improve the text flow.

| ID | Name | Technical Description | AI Signal Context | Fix (How to fix it) |
|:---|:---|:---|:---|:---|
| **PatternEN-1** | Significance inflation | Inflated claims about legacy, "broader trends", or "pivotal moments". | LLMs "puff up" the importance of mundane or specific topics. | Remove the inflated claim. State concrete facts instead. |
| **PatternEN-2** | Notability name-dropping | Listing media outlets (NYT, BBC) without context or specific quotes. | Fake authority by listing famous names instead of citing evidence. | Cite one specific claim from one source instead of a list. |
| **PatternEN-3** | Superficial -ing analyses | Tacking participial phrases (highlighting, underscoring) onto sentences. | Used to fake depth or "wrap up" a sentence with a vague benefit. | Remove the trailing phrase. Give the point its own sentence with specifics. |
| **PatternEN-4** | Promotional language | Ad-copy style: "nestled in the heart of", "breathtaking". | Tourism brochure/press release tone common in marketing-heavy training data. | Replace with neutral, factual descriptions. |
| **PatternEN-5** | Vague attributions | "Experts believe", "Industry reports suggest". | Lack of specific sources. AI hallucinates authority. | Name the specific source or study. If you can't find it, remove the claim. |
| **PatternEN-6** | Formulaic challenges | "Despite challenges... continues to thrive". | Predictable "setback -> pivot to optimism" structure. | Replace with specific challenges and concrete, measurable outcomes. |
| **PatternEN-7** | AI vocabulary | Words like "delve", "tapestry", "landscape", "seamless". | High-frequency usage of specific "buzzy" words by LLMs. | Replace with simpler, more direct synonyms. |
| **PatternEN-8** | Copula avoidance | "Serves as", "Boasts" instead of "is", "has". | Over-complicating simple verbs to sound more formal or distinctive. | Use simple "is", "are", or "has" instead. |
| **PatternEN-9** | Negative parallelisms | "It's not just X, it's Y" / "Not only X but Y". | Formulaic way to structure ideas often overused by LLMs. | Rewrite directly. State what it IS, not what it "isn't just". |
| **PatternEN-10** | Rule of three | Grouping abstract nouns/adjectives in compulsory triplets. | AI loves triads for a perceived sense of completeness. | Pick the one or two words that matter. Triplets feel mechanical. |
| **PatternEN-11** | Synonym cycling | Using different words for the same thing in consecutive sentences. | Mechanical attempt to avoid repetition seen in training data rules. | Pick one term and stick with it for clarity. |
| **PatternEN-12** | False ranges | "From the dawn of time to the digital age". | Broad, non-meaningful scales used as filler introductions. | Be specific about the actual time frame or topics covered. |
| **PatternEN-13** | Em dash overuse | Excessive use of — characters as a crutch for "punchy" writing. | High density of em dashes is a common stylistic quirk of modern LLMs. | Replace most with commas, periods, or parentheses. |
| **PatternEN-14** | Boldface overuse | Mechanical bolding of keywords or phrases. | Using bold as a crutch for emphasis instead of letting the prose work. | Remove bolding. Let the sentence structure carry the emphasis. |
| **PatternEN-15** | Inline-header lists | Bullets starting with **Bold Header:** content. | Over-formatted responses that feel like a textbook or automated summary. | Use prose paragraphs; reserve lists for actual enumerations. |
| **PatternEN-16** | Title Case headings | Capitalizing Every Word In A Heading. | Chatbots often default to Title Case regardless of style guide. | Use sentence case (capitalize only first word and proper nouns). |
| **PatternEN-17** | Emoji overuse | Using emojis in professional or technical headers/bullets. | Artifact of "friendly assistant" persona. | Remove emojis from professional/technical writing. |
| **PatternEN-18** | Curly quotes | Unicode curly quotes instead of straight ones. | Default behavior for several models (ChatGPT). | Replace with standard straight quotes. |
| **PatternEN-19** | Chatbot artifacts | "I hope this helps!", "Here is an overview". | Leftover conversational filler from the model's persona. | Remove — start directly with the content. |
| **PatternEN-20** | Cutoff disclaimers | "As an AI...", "My knowledge cutoff...". | Explicit identity markers of the chatbot. | Remove completely. |
| **PatternEN-21** | Sycophantic tone | "Great question!", "You're absolutely right!". | People-pleasing language to lower user friction. | Remove — address the substance of the text directly. |
| **PatternEN-22** | Filler phrases | "In order to" (to), "Due to the fact that" (because). | Verbose phrases that add word count without adding meaning. | Shorten to the most direct version. |
| **PatternEN-23** | Excessive hedging | "Could potentially possibly", "might arguably". | Stacking qualifiers to avoid making a definite statement. | Use one qualifier or remove them for a direct claim. |
| **PatternEN-24** | Generic conclusions | "The future looks bright", "Exciting times ahead". | AI avoids taking a stand and prefers vague, upbeat endings. | End with a specific fact, concrete result, or a call to action. |
| **PatternEN-25** | Reasoning artifacts | "Let me think", "Step 1:", "Breaking this down". | Exposed chain-of-thought artifacts in the final output. | Remove the reasoning or make it natural prose. |
| **PatternEN-26** | Excessive structure | Too many headers/bullets for short content. | Mechanical over-organization of simple information. | Let the content flow naturally. Use prose. |
| **PatternEN-27** | Confidence calibration | "I'm confident that", "It's worth noting". | Prefacing statements with meta-analysis of their importance. | Just state the fact directly. |
| **PatternEN-28** | Acknowledgment loops | Restating the user's question before answering. | Mechanical confirmation of the input. | Answer directly without repeating the prompt. |
| **PatternEN-29** | Unicode obfuscation | Zero-width characters, soft hyphens. | Used by some tools to try and game AI detectors. | Remove — clean the text of hidden characters. |
