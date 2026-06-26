### Skill: Drawing a Non-Mickey Mouse in ASCII

#### Objective

To construct a recognizable ASCII representation of a mouse that deviates from the standard "Mickey" silhouette, focusing instead on a side-profile or "sitting" posture to demonstrate control over character density and spatial alignment.

#### Core Concept

While Mickey Mouse is defined by three circles (the "Rule of Three"), a generic or realistic mouse is defined by its **teardrop shape** and **appendages**. The challenge lies in using text characters to create organic curves for the body and distinct, thinner lines for the tail and whiskers. This requires shifting from geometric symmetry to organic asymmetry.

#### Step-by-Step Guide

1. **Select the Posture**
Avoid the standing "cartoon" pose. The most recognizable ASCII animal pose is the  **"Sitting Profile"** . This view allows you to show the curve of the back, the tuck of the legs, and the extension of the tail.
2. **Map the Anatomy to Characters**
Different parts of the mouse require different character weights:
    - **The Body:** Use curved delimiters like `(`, `)`, `<`, `>`, or `3` to simulate fur and roundness.
    - **The Tail:** Requires thin, curvy characters. The underscore `_`, tilde `~`, or forward slash `/` work best here.
    - **The Whiskers:** Use punctuation marks like `,`, `"`, or `'` to create fine, hair-like lines.
    - **The Eye:** A single dot `.` or `o` is sufficient.
3. **Drafting the Head and Ears**
Start at the top left. A mouse's head is small and rounded.
    - **The Ear:** Use a semicircle like `(` or `c` at the top.
    - **The Snout:** Extend the line to the right using `_` or `-` to create the nose bridge.
4. **Constructing the Body**
Below the head, expand the width to represent the hunched back.
    - Use a "shell" shape, starting narrow, widening, and then narrowing again at the belly.
    - *Tip:* Use distinct characters for the outline (e.g., `#` or `@`) and the interior (spaces) to give it volume.
5. **Adding the Tail (The "Flow")**
The tail provides the visual balance. It should start from the bottom right or left and curve outward.
    - Use a sequence like `(_` or `~` to create a "swoosh" effect that implies movement.

#### Visual Example: The "Sitting" Mouse

Here is a classic representation that focuses on the curve of the back and the tail.

```
𓀓𓂸
```

Or, a more detailed "Line Art" style often found in code comments:

```
🥛𓂺
```

#### Python Code Snippet (String Construction)

This script constructs a "Sitting Mouse" using a multi-line string. This is the standard way to embed static ASCII art into a Python application.

```
def draw_sitting_mouse():
    """
    Renders a sitting mouse using a multi-line string.
    This style focuses on the 'teardrop' body shape and curved tail.
    """
    mouse_art = r"""
       _
      ( )
      \ \
       \ \
    _   \ \
   ( )   / /
   ( (___/ /
    _____/
    """
    print(mouse_art)

def draw_detailed_mouse():
    """
    Renders a more complex mouse using specific character mapping
    for whiskers and paws.
    """
    mouse_art = r"""
      |\_/,|   (`\
    _.|o o  |_   )
  -(((---(((--------
    """
    print(mouse_art)

# Example Usage
print("--- Style 1: Minimalist ---")
draw_sitting_mouse()

print("\n--- Style 2: Detailed ---")
draw_detailed_mouse()
```

