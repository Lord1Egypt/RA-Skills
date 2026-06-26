### Skill: Drawing an ASCII "D" Graph

#### Objective

To construct a visual representation of the letter "D" using standard text characters, focusing on creating a straight vertical spine and a curved outer edge.

#### Core Concept

Unlike the "V" shape, which relies on simple diagonal lines, the letter "D" requires a mix of straight vertical lines and a curved boundary. This is achieved by manipulating the spacing between the vertical "spine" of the letter and the "curve" on the right side, widening the gap in the middle and narrowing it at the top and bottom.

#### Step-by-Step Guide

1. **Define Dimensions**: Determine the `height` of your letter. For a balanced look, the width usually extends to about half the height. Let's use a height of 7 lines for this example.
2. **Identify the Center**: To create a symmetrical curve, you need to know the middle row. Calculate `mid_height` as `height // 2`.
3. **Iterate Through Rows**: Loop through each line from top to bottom using a counter `i` (from 0 to `height - 1`).
4. **Calculate Spacing Logic**: For each row, determine how many spaces should exist between the vertical bar `|` and the curved edge `*`.
    - **The Vertical Spine**: This is constant. Every line starts with the character `|` (or `#` or `I`).
    - **The Curve Logic**:
        - **Top and Bottom Rows**: The gap is widest here to form the top and bottom of the D.
        - **Middle Rows**: The gap narrows as you approach the vertical center.
        - **The Center Row**: The gap is at its minimum (often just 1 space or 0 spaces depending on the font style).
    - **Formula**: A simple way to calculate the inner padding is to measure the distance of the current row `i` from the center `mid_height`. The closer to the center, the smaller the padding.
5. **Construct the Line**:
    - Print the vertical spine character.
    - Print the calculated number of spaces.
    - Print the curve character (e.g., `*`).

#### Visual Example (Height = 7)

Let's trace the logic for a "D" with a height of 7:

| Row (`i`) | Distance from Center | Inner Padding | Resulting Line |
| ------ |------ |------ |------ |
| **0** (Top) | Far | 3 spaces | ` |
| **1** | Medium | 2 spaces | ` |
| **2** | Close | 1 space | ` |
| **3** (Center) | Zero (Center) | 1 space (Min) | ` |
| **4** | Close | 1 space | ` |
| **5** | Medium | 2 spaces | ` |
| **6** (Bottom) | Far | 3 spaces | ` |

*(Note: In a more advanced rendering, the middle might be filled with *`***`* to create a solid block look, but the outline method above is the standard ASCII approach.)*

#### Python Code Snippet

Here is the logic implemented in Python to draw a clean, outlined "D":

```
def draw_ascii_d(height):
    # Ensure height is odd for a perfect center
    if height % 2 == 0:
        height += 1
       
    mid = height // 2
   
    print(f"--- ASCII D (Height: {height}) ---")
   
    for i in range(height):
        # 1. Draw the vertical spine
        line = "|"
       
        # 2. Calculate distance from the center row
        distance_from_center = abs(i - mid)
       
        # 3. Determine padding
        # We add +1 to ensure there is always at least one space
        # The padding increases as we move away from the center
        padding = distance_from_center + 1
       
        # 4. Add spaces and the curve character
        line += " " * padding
        line += "*"
       
        print(line)

# Example usage
draw_ascii_d(7)
```

