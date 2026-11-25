# -*- coding: utf-8 -*-
"""Example driver: one-page demo lesson in the hand-drawn notes template.

Copy this file per lecture, rewrite the content from the transcript, keep
the helper calls. Run:  python example_board.py [outdir]
Then print the generated HTML to PDF with headless Chrome (see SKILL.md).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import make_notes as mb

mb.reset()

# ---------------- PAGE 1 ----------------
p = 0
fr = mb.frame(p, "Page 1 - Example lesson")
y = mb.title("Example Lesson Title", page=p, frame=fr)
sub = "Video N --> Short subtitle of the lesson"
sw = len(sub) * 15 * mb.MONO_FACTOR
y = mb.text((mb.PAGE_W - sw) / 2, y + 10, sub, 15, mb.BLUE, page=p,
            align="center", width=sw, frame=fr)
y += 34

y = mb.heading("MAIN SECTION (orange)", mb.ORANGE, page=p, frame=fr, y=y)
y += 12
y = mb.text(mb.MARGIN, y,
    "Task: one or two lines framing the problem the lesson solves.\n"
    "Keep the transcript's reasoning; do not invent content.",
    16, mb.BLUE, page=p, frame=fr)
y += 26

y = mb.heading("SUB-SECTION WITH STEPS", mb.ORANGE, page=p, frame=fr,
               y=y, size=20)
y += 12
y = mb.text(mb.MARGIN, y,
    "* First key idea\n"
    "    --> Definition line using the arrow style\n"
    "* Second key idea\n"
    "    --> Eg: a concrete example from the lesson",
    16, mb.BLUE, page=p, frame=fr)
y += 30

# Diagram: three yellow nodes left -> right
nh = 56
mb.node(mb.MARGIN + 100, y, 170, nh, "Input", page=p, frame=fr)
mb.node(mb.MARGIN + 340, y, 190, nh, "Model / Process", page=p, frame=fr)
mb.node(mb.MARGIN + 580, y, 170, nh, "Output", page=p, frame=fr)
mb.arrow(mb.MARGIN + 185, y + nh / 2, mb.MARGIN + 245, y + nh / 2,
         page=p, frame=fr)
mb.arrow(mb.MARGIN + 435, y + nh / 2, mb.MARGIN + 495, y + nh / 2,
         page=p, frame=fr)
y += nh + 28

y = mb.heading("PROBLEM / DRAWBACKS (red)", mb.RED, page=p, frame=fr,
               y=y, size=20)
y += 10
y = mb.text(mb.MARGIN, y,
    "1. First drawback in red\n"
    "2. Second drawback in red",
    16, mb.RED, page=p, frame=fr)
y += 24

y = mb.heading("SOLUTION (green)", mb.GREEN, page=p, frame=fr, y=y, size=20)
y += 10
y = mb.text(mb.MARGIN, y,
    "--> How the lesson resolves the problem\n"
    "--> Why the solution scales / works better",
    16, mb.BLUE, page=p, frame=fr)
y += 24

# Command box (only when the lesson actually shows commands)
y = mb.command_box(mb.MARGIN, y, 420,
    "pip install example\npython run_demo.py",
    label="Commands:", page=p, frame=fr)

outdir = sys.argv[1] if len(sys.argv) > 1 else "."
mb.save("00-example-lesson", outdir)
