---
name: architect-4r
description: Use only when explicitly invoked. Describe existing software architecture from code or context using Li Yunhua's 4R method. Align on views, roles, and key scenarios, then draw architecture and scenario diagrams.
metadata:
  language: en
  translation_of: architect-4r-cn
  version: "0.4.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/architect-4r
---

# 4R system modeling framework

Describe existing architecture from code or context the user provides. Use Li Yunhua's [4R method](https://time.geekbang.org/column/article/6458) to explain the selected system's top-level structure and operating rules.

| Element | What to explain |
| --- | --- |
| Rank | The level of decomposition you are looking at. The top level is relative to the selected system. A role at one level can expand into a system at the next. |
| Role | The units that make up this level and the responsibilities each carries. |
| Relation | The connections between roles, such as calls, notifications, sharing, or dependencies. |
| Rule | How roles work together to deliver a system function, including triggers, order, outcomes, and failures that affect the result. |

A perspective sets the focus. The level determines how far you break down the system. Use one level of detail per architecture diagram. Ground roles, relations, and rules in code, configuration, documentation, or the user's account. Mark inferences and gaps where they appear. If a gap changes a role boundary or a key interaction, ask one focused question first.

## Workflow

1. **Select views.** State the question to answer. List relevant options, such as business, system, application, and physical deployment. Give each option a system boundary, level of detail, and question it answers. Recommend one or two options and invite the user to select one or more, add an option, or leave a note. Reuse any choices the user has made.
2. **Align on roles.** After view selection, list every internal role supported by the evidence at that view's level. Give each role a one-sentence responsibility. Name the owner of any key state. List external participants separately and flag gaps. If the evidence supports different groupings, recommend one, offer one alternative, and explain how the responsibilities differ. Ask the user to review the roster and invite additions, merges, splits, or notes.
3. **Draw relations.** After aligning on roles, draw one architecture diagram per view. Use its title and boundary for Rank, and nodes and directed edges for Role and Relation. Label edges by purpose and distinguish runtime communication from source dependencies as appropriate to the view.
4. **Select scenarios and draw rules.** List supported key scenarios by view. Say which part of the collaboration each scenario explains and mark your recommendations. Let the user select multiple scenarios, add one, or name a branch to focus on. Reuse scenarios the user has specified. Draw one Rule diagram per selected scenario and choose the diagram type yourself. Use a sequence diagram for interactions, a flowchart for decisions, or a state diagram for transitions.

When you start drawing, read the [diagram reference](references/diagrams.md) for notation, diagram selection, and an example. Before delivery, check that the architecture diagram covers the agreed roles, names match across diagrams, and key scenario interactions map to relations in the architecture diagram.
