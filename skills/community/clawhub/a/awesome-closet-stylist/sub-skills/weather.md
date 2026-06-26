# weather

## Purpose and Scope

This sub-specification defines how the agent should handle weather-dependent context when weather may materially affect outfit guidance or when the user explicitly asks for weather-aware help.

This document defines tool and fallback boundaries. It does not define a fixed tool sequence.

## Operating Principles

The weather module must follow these principles:

- **local-first:** prefer authoritative local configuration and locally available context before external retrieval.
- **user-provided-first:** if the user already supplied sufficient weather context, use it directly.
- **capability-aware:** do not assume any specific API, browser, search path, or external retrieval tool is available.
- **non-overriding external context:** external weather results may inform recommendation reasoning, but must not override wardrobe facts or other authoritative local state.
- **graceful degradation:** when one retrieval path fails, degrade safely instead of assuming failure means no useful answer is possible.
- **clarify only when needed:** ask the user only when the missing weather context materially affects the answer and cannot be filled safely.

## When Weather Context Is Needed

Weather context is relevant when any of the following is true:

- the user explicitly asks about current or upcoming weather,
- the user explicitly wants a weather-aware outfit recommendation,
- the recommendation outcome would materially differ based on temperature, wind, rain, or similar conditions,
- or the user provided partial weather context that is clearly intended to shape the recommendation.

If weather context is not relevant to the user’s request, the agent should not force weather retrieval.

## Weather Context Priority Order

When weather context is needed, use this priority order:

1. **User-provided weather context in the current conversation**
2. **Relevant local configuration or already available local weather context**
3. **Capability-appropriate external retrieval**
4. **User clarification when the gap remains material**

The agent should not query externally when the user has already provided enough context to support a good recommendation.

If the user provides approximate but usable weather information such as “around 18°C and windy,” the agent should normally use it as-is.

## Capability-Aware External Retrieval

If externally retrieving weather is necessary, the agent may choose any available path that fits the current environment and user authorization.

Examples may include:
- a configured weather API from local config,
- an allowed browser-based lookup,
- an allowed web retrieval tool,
- or another environment-supported external lookup path.

This sub-spec does not require a fixed provider order beyond the global priority rules above.

When multiple configured providers are available, the agent may try them in a reasonable order. The purpose is to obtain enough trustworthy weather context for the current task, not to exhaust every provider mechanically.

External weather retrieval should remain narrow in scope. Retrieve only the context needed for the current recommendation or answer.

## Failure Downgrade and Clarification Rules

When an external retrieval path fails, the agent should downgrade in this order of reasoning:

1. use already sufficient user-provided context if available,
2. try another capability-appropriate retrieval path if one is available and justified,
3. continue with a qualified answer if weather is helpful but not critical,
4. ask the user for missing weather context if the gap is material,
5. avoid pretending that missing weather data was successfully retrieved.

Ask the user for clarification when:
- city or location is necessary and not safely inferable,
- the available weather context is too incomplete for a materially weather-sensitive recommendation,
- or all appropriate retrieval paths fail and the missing context still matters.

A suitable fallback prompt is:

> I can still help, but I do not have enough reliable weather context for this recommendation. Please tell me the approximate temperature and any important conditions such as wind or rain.

## How Weather Context May Be Used

Weather context may be used to:
- adjust warmth assumptions,
- account for wind, rain, humidity, or layering needs,
- explain why a recommended item is more or less suitable,
- and qualify tradeoffs between comfort, occasion, and style.

The agent should integrate weather naturally into the reasoning and response. It does not need to separately announce that a weather lookup happened unless that is relevant to transparency or failure handling.

## What Weather Context Must Not Do

Weather context must not:
- override wardrobe facts,
- invent owned items,
- justify recommendations that assume unavailable clothing,
- silently convert temporary weather context into durable user preference,
- or trigger unauthorized automation.

External results are contextual input, not authority over local wardrobe state.

## Configuration and Lightweight User Guidance

If local weather configuration is missing or incomplete, the agent may give a lightweight suggestion about available configuration options when that would help the user.

Such guidance should:
- stay brief,
- clarify that local configuration remains local,
- avoid pressuring the user into setup when a non-persistent fallback is sufficient,
- and follow skill-lifecycle memory rules so the same setup suggestion is not repeated every session once it has already been detected and surfaced.

## Interfaces to Main Spec and Write Modules

This sub-spec inherits the global tool and automation boundary from `SKILL.md`.

This sub-spec does not define persistence rules for notes, preferences, or CRUD changes. If weather-related automation or fallback organization produces a possible write candidate, that candidate must still be handled according to the write, confirmation, deduplication, and persistence rules defined elsewhere.
