# Task Decomposition Examples

## Example 1: Kitchen Task

**Input:**
- **Image**: Kitchen scene with toaster, fruits, plate on white table
- **Task**: "Take toasted bread from bread machine on white table place on plate"

**Decomposition:**
1. approach the toaster on the white table with either gripper
2. grasp the toasted bread from the toaster with right gripper
3. lift the toasted bread with right gripper
4. move to the plate with either gripper
5. place the toasted bread on the plate with right gripper
6. release the toasted bread with right gripper

---

## Example 2: Assembly Task

**Input:**
- **Image**: Turntable with cube-shaped block
- **Task**: "Grasp the rotating cube-shaped block on the turntable and place it on the table"

**Decomposition:**
1. approach the turntable with either gripper
2. wait for the block to rotate into graspable position with either gripper
3. grasp the cube-shaped block with right gripper
4. lift the block with right gripper
5. move to the table with either gripper
6. place the block on the table with right gripper
7. release the block with right gripper

---

## Example 3: Cleaning Task

**Input:**
- **Image**: Table with brown water stains
- **Task**: "Wipe off the brown water stains in the middle of the table with a purple rag"

**Decomposition:**
1. approach the table with either gripper
2. grasp the purple rag with right gripper
3. move to the center of the table with right gripper
4. wipe the brown water stains in the middle of the table with right gripper
5. release the rag with right gripper

---

## Example 4: Outdoor/Delivery Task

**Input:**
- **Image**: Porch with package
- **Task**: "Pick up a delivery from the front porch and bring it inside"

**Decomposition:**
1. approach the front porch with either gripper
2. grasp the delivery package with right gripper
3. lift the package with right gripper
4. move toward the indoors with either gripper
5. place the package inside with right gripper
6. release the package with right gripper

---

## Example 5: Grocery Task

**Input:**
- **Image**: White checkered table with bag of fruit
- **Task**: "Take the fruit out of the bag on the white checkered tablecloth and place them on the plate"

**Decomposition:**
1. approach the white checkered table with either gripper
2. grasp the bag of fruit with left gripper
3. open the bag with left gripper
4. grasp a fruit from the bag with right gripper
5. move to the plate with right gripper
6. place the fruit on the plate with right gripper
7. release the fruit with right gripper
8. repeat steps 4-7 for remaining fruits
9. release the bag with left gripper

---

## Notes

- Always specify gripper (left/right/either)
- Include location info in parentheses when relevant
- Break into atomic actions (one action per subtask)
- Use actions only from the action bank