# VHS tape — RA-Skills CLI demo. Regenerate with:  vhs demo/ra-skills.tape
Output demo/ra-skills.gif

Set Shell bash
Set FontSize 17
Set Width 1180
Set Height 820
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 55ms

# --- setup (hidden): put ra-skills on PATH, clean minimal prompt ---
Hide
Type "export PATH=$HOME/.local/bin:$PATH; PS1='\033[36m$\033[0m '" Enter
Ctrl+L
Show
Sleep 700ms

Type "ra-skills --version" Enter
Sleep 1.5s
Ctrl+L
Sleep 400ms

Type "ra-skills stats" Enter
Sleep 3.5s
Ctrl+L
Sleep 400ms

Type "ra-skills search github --limit 2" Enter
Sleep 4s
Ctrl+L
Sleep 400ms

Type "ra-skills show aso-playbook" Enter
Sleep 3.5s
Ctrl+L
Sleep 400ms

Type "ra-skills list --source built-in --limit 8" Enter
Sleep 4s
