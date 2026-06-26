# Film Language For Chain-Referenced Shortform

Use this file when the user needs stronger `storyboard`, `blocking`, `lensing`, or `camera movement` guidance.

## Purpose

The goal is not to make prompts longer. The goal is to make each shot more legible and easier for the model to preserve across cuts.

## Shot card template

Write a shot card before writing the shot prompt:

- `beat`: what changes emotionally or narratively
- `shot_size`: ECU / CU / MCU / MS / MLS / LS / WS / EWS
- `angle`: eye level / low / high / overhead / dutch / OTS / POV
- `lens_feel`: intimate / neutral / compressed / expansive
- `movement`: static / pan / tilt / push-in / pull-back / lateral track / orbit / handheld
- `blocking`: where the actor starts, moves, and ends
- `screen_direction`: left-to-right, right-to-left, toward camera, away from camera
- `must_show`: props, hands, eyeline targets, background landmarks
- `bridge_frame_goal`: what pose or composition should survive into the next shot

If the shot card is weak, the prompt will become noisy.

## Shot size guidance

- `ECU`: details, symbols, decisive micro-actions
- `CU`: emotional recognition, reaction, realization
- `MCU`: intimate dialogue, restrained movement
- `MS`: default for readable action plus emotion
- `MLS`: walking, hand gestures, tactical interaction
- `LS / WS`: geography, threat, environment, isolation
- `EWS`: scale, loneliness, transitions

Do not stack multiple close framings in a row unless you deliberately want pressure or claustrophobia.

## Angle guidance

- `eye level`: neutral, observational, honest
- `low angle`: power, threat, heroism
- `high angle`: fragility, exposure, defeat
- `overhead`: choreography, surveillance, spatial clarity
- `dutch`: instability, panic, distortion
- `OTS`: relational tension and dialogue perspective
- `POV`: subjectivity, immersion, eyeline payoff

Use angle changes sparingly in shortform. Small angle changes cut better than dramatic flips.

## Movement guidance

- `static`: confidence, tension, observation
- `push-in`: realization, pressure, dread, intimacy
- `pull-back`: loss, aftermath, emotional distance
- `pan / tilt`: reveal information already present in the scene
- `lateral track`: accompany movement through space
- `orbit`: spectacle or emotional suspension; use carefully
- `handheld`: instability, urgency, documentary feel

In AI video, movement is expensive. Prefer one clear move over several partial moves.

## Blocking guidance

- One actor: define start pose, vector of motion, end pose.
- Two actors: define dominance, distance, eyeline, and who owns foreground.
- Prop interaction: define which hand, when contact happens, and whether the prop remains visible after contact.

If a prop matters in the next shot, keep it visible near the end of the current shot.

## Geography rules

- Lock a `side of line` for dialogue or conflict.
- Preserve `screen direction` across adjacent shots.
- Use at least one shot per scene that clearly explains entrances, exits, and background anchors.
- If geography is confusing, widen the frame or reduce camera movement.

## Edit-minded design

Each shot should end with a bridgeable state:

- readable face or pose
- readable prop position
- readable light state
- readable vector of motion

Bad bridge frames are often the real reason the next shot drifts.

## Aspect ratio notes

- `16:9`: favors geography, ensemble spacing, lateral movement
- `9:16`: favors singles, vertical movement, center-weighted composition

Do not write the same composition instructions for both formats. Re-compose them.

## Fast diagnosis

- Feels generic: weak beat or weak framing choice
- Feels messy: too many simultaneous changes
- Feels fake: motion language and blocking disagree
- Feels discontinuous: cut relationship was never designed
