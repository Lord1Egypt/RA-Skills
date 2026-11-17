# Smell-to-Refactoring Map

Candidate techniques are advisory. Select by observed cause, preconditions, risk, and the smallest safe transformation; never reduce diagnosis to keyword lookup.

## SMELL-MYSTERIOUS-NAME — Mysterious Name

**Primary/Supporting Candidates**
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-RENAME-VARIABLE`
- `RF-RENAME-FIELD`

**Selection Note**
- Confirm the diagnosed cause of Mysterious Name and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-DUPLICATED-CODE — Duplicated Code

**Primary/Supporting Candidates**
- `RF-EXTRACT-FUNCTION`
- `RF-SLIDE-STATEMENTS`
- `RF-PULL-UP-METHOD`

**Selection Note**
- Confirm the diagnosed cause of Duplicated Code and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-LONG-FUNCTION — Long Function

**Primary/Supporting Candidates**
- `RF-EXTRACT-FUNCTION`
- `RF-REPLACE-TEMP-WITH-QUERY`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-PRESERVE-WHOLE-OBJECT`
- `RF-REPLACE-FUNCTION-WITH-COMMAND`
- `RF-DECOMPOSE-CONDITIONAL`
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`
- `RF-SPLIT-LOOP`

**Selection Note**
- Confirm the diagnosed cause of Long Function and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-LONG-PARAMETER-LIST — Long Parameter List

**Primary/Supporting Candidates**
- `RF-REPLACE-PARAMETER-WITH-QUERY`
- `RF-PRESERVE-WHOLE-OBJECT`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-REMOVE-FLAG-ARGUMENT`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`

**Selection Note**
- Confirm the diagnosed cause of Long Parameter List and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-GLOBAL-DATA — Global Data

**Primary/Supporting Candidates**
- `RF-ENCAPSULATE-VARIABLE`

**Selection Note**
- Confirm the diagnosed cause of Global Data and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-MUTABLE-DATA — Mutable Data

**Primary/Supporting Candidates**
- `RF-ENCAPSULATE-VARIABLE`
- `RF-SPLIT-VARIABLE`
- `RF-SLIDE-STATEMENTS`
- `RF-EXTRACT-FUNCTION`
- `RF-SEPARATE-QUERY-FROM-MODIFIER`
- `RF-REMOVE-SETTING-METHOD`
- `RF-REPLACE-DERIVED-VARIABLE-WITH-QUERY`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`
- `RF-COMBINE-FUNCTIONS-INTO-TRANSFORM`
- `RF-CHANGE-REFERENCE-TO-VALUE`

**Selection Note**
- Confirm the diagnosed cause of Mutable Data and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-DIVERGENT-CHANGE — Divergent Change

**Primary/Supporting Candidates**
- `RF-SPLIT-PHASE`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`
- `RF-EXTRACT-CLASS`

**Selection Note**
- Confirm the diagnosed cause of Divergent Change and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-SHOTGUN-SURGERY — Shotgun Surgery

**Primary/Supporting Candidates**
- `RF-MOVE-FUNCTION`
- `RF-MOVE-FIELD`
- `RF-COMBINE-FUNCTIONS-INTO-CLASS`
- `RF-COMBINE-FUNCTIONS-INTO-TRANSFORM`
- `RF-SPLIT-PHASE`
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`

**Selection Note**
- Confirm the diagnosed cause of Shotgun Surgery and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-FEATURE-ENVY — Feature Envy

**Primary/Supporting Candidates**
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`

**Selection Note**
- Confirm the diagnosed cause of Feature Envy and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-DATA-CLUMPS — Data Clumps

**Primary/Supporting Candidates**
- `RF-EXTRACT-CLASS`
- `RF-INTRODUCE-PARAMETER-OBJECT`
- `RF-PRESERVE-WHOLE-OBJECT`

**Selection Note**
- Confirm the diagnosed cause of Data Clumps and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-PRIMITIVE-OBSESSION — Primitive Obsession

**Primary/Supporting Candidates**
- `RF-REPLACE-PRIMITIVE-WITH-OBJECT`
- `RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES`
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`
- `RF-EXTRACT-CLASS`
- `RF-INTRODUCE-PARAMETER-OBJECT`

**Selection Note**
- Confirm the diagnosed cause of Primitive Obsession and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-REPEATED-SWITCHES — Repeated Switches

**Primary/Supporting Candidates**
- `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`

**Selection Note**
- Confirm the diagnosed cause of Repeated Switches and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-LOOPS — Loops

**Primary/Supporting Candidates**
- `RF-REPLACE-LOOP-WITH-PIPELINE`

**Selection Note**
- Confirm the diagnosed cause of Loops and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-LAZY-ELEMENT — Lazy Element

**Primary/Supporting Candidates**
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`
- `RF-COLLAPSE-HIERARCHY`

**Selection Note**
- Confirm the diagnosed cause of Lazy Element and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-SPECULATIVE-GENERALITY — Speculative Generality

**Primary/Supporting Candidates**
- `RF-COLLAPSE-HIERARCHY`
- `RF-INLINE-FUNCTION`
- `RF-INLINE-CLASS`
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-REMOVE-DEAD-CODE`

**Selection Note**
- Confirm the diagnosed cause of Speculative Generality and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-TEMPORARY-FIELD — Temporary Field

**Primary/Supporting Candidates**
- `RF-EXTRACT-CLASS`
- `RF-MOVE-FUNCTION`
- `RF-INTRODUCE-SPECIAL-CASE`

**Selection Note**
- Confirm the diagnosed cause of Temporary Field and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-MESSAGE-CHAINS — Message Chains

**Primary/Supporting Candidates**
- `RF-HIDE-DELEGATE`
- `RF-EXTRACT-FUNCTION`
- `RF-MOVE-FUNCTION`

**Selection Note**
- Confirm the diagnosed cause of Message Chains and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-MIDDLE-MAN — Middle Man

**Primary/Supporting Candidates**
- `RF-REMOVE-MIDDLE-MAN`
- `RF-INLINE-FUNCTION`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`

**Selection Note**
- Confirm the diagnosed cause of Middle Man and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-INSIDER-TRADING — Insider Trading

**Primary/Supporting Candidates**
- `RF-MOVE-FUNCTION`
- `RF-MOVE-FIELD`
- `RF-HIDE-DELEGATE`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`

**Selection Note**
- Confirm the diagnosed cause of Insider Trading and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-LARGE-CLASS — Large Class

**Primary/Supporting Candidates**
- `RF-EXTRACT-CLASS`
- `RF-EXTRACT-SUPERCLASS`
- `RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES`

**Selection Note**
- Confirm the diagnosed cause of Large Class and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-ALTERNATIVE-CLASSES-DIFFERENT-INTERFACES — Alternative Classes with Different Interfaces

**Primary/Supporting Candidates**
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-SUPERCLASS`

**Selection Note**
- Confirm the diagnosed cause of Alternative Classes with Different Interfaces and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-DATA-CLASS — Data Class

**Primary/Supporting Candidates**
- `RF-ENCAPSULATE-RECORD`
- `RF-REMOVE-SETTING-METHOD`
- `RF-MOVE-FUNCTION`
- `RF-EXTRACT-FUNCTION`
- `RF-SPLIT-PHASE`

**Selection Note**
- Confirm the diagnosed cause of Data Class and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-REFUSED-BEQUEST — Refused Bequest

**Primary/Supporting Candidates**
- `RF-PUSH-DOWN-METHOD`
- `RF-PUSH-DOWN-FIELD`
- `RF-REPLACE-SUBCLASS-WITH-DELEGATE`
- `RF-REPLACE-SUPERCLASS-WITH-DELEGATE`

**Selection Note**
- Confirm the diagnosed cause of Refused Bequest and choose only a technique whose preconditions fit the current ownership and behavior contract.

## SMELL-COMMENTS — Comments

**Primary/Supporting Candidates**
- `RF-EXTRACT-FUNCTION`
- `RF-CHANGE-FUNCTION-DECLARATION`
- `RF-INTRODUCE-ASSERTION`

**Selection Note**
- Confirm the diagnosed cause of Comments and choose only a technique whose preconditions fit the current ownership and behavior contract.
