"""Word lists for Communication DNA analysis engine."""

STOP_WORDS = frozenset("""
a about above after again against all am an and any are aren't as at be because been before being
below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down
during each few for from further get got had hadn't has hasn't have haven't having he he'd he'll
he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't
it it's its itself let's me more most mustn't my myself no nor not of off on once only or other
ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some
such than that that's the their theirs them themselves then there there's these they they'd they'll
they're they've this those through to too under until up very was wasn't we we'd we'll we're we've
were weren't what what's when when's where where's which while who who's whom why why's will with
won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
just really also still even much well back now get got go going one two three four five make way
thing things people like know going going been been would could should
""".split())

FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "actually", "literally",
    "so", "right", "i mean", "kind of", "sort of",
]

HEDGING_PHRASES = [
    "i think", "maybe", "probably", "might", "not sure", "i guess",
    "perhaps", "it seems", "i believe", "it looks like", "i suppose",
    "could be", "it might", "possibly",
]

ASSERTIVE_PHRASES = [
    "definitely", "absolutely", "we must", "clearly", "obviously",
    "certainly", "without a doubt", "no question", "for sure", "undoubtedly",
    "we need to", "it's clear", "the fact is", "without doubt",
]

COMMITMENT_PATTERNS = [
    "i'll", "i will", "let me", "i'm going to", "we'll", "we will",
    "we should", "action item", "follow up", "by monday", "by tuesday",
    "by wednesday", "by thursday", "by friday", "next week", "tomorrow",
    "i'm gonna", "we're going to", "i can do", "i'll take care",
    "let's plan", "we need to", "i'll handle", "i'll send", "i'll check",
]

DECISION_PATTERNS = [
    "we decided", "let's go with", "the plan is", "we're going with",
    "the decision is", "we agreed", "final answer", "we'll do",
    "so we're doing", "that's the plan", "let's proceed with",
]

FORMAL_WORDS = frozenset("""
accordingly additionally aforementioned albeit approximately commence concerning consequently
constitutes demonstrate determine effective elaborate endeavor ensure establish facilitate
furthermore herein hitherto however illustrate implement implications incorporate
indicate infrastructure initiate inquire investigate magnitude maintain methodology
moreover nevertheless notwithstanding objective obtained optimal parameter
participation pertaining predominantly preliminary prior proceed procurement
proficiency pursuant regarding remuneration requisite respectively
significantly simultaneously subsequent sufficient supplementary
thereby therefore thorough thus undertaken utilize verification
whereas whereby accommodate acknowledge aforementioned allocate
amendment appraise ascertain assessment authorize benchmark
circumvent collaborate comprehensive compulsory concur conducive
consolidate contingency convene corroborate criterion culminate
delineate designate disseminate efficacy elucidate encompass
envisage expedite formulate henceforth imperative inaugurate
infrastructure instantiate integrate jurisdiction legislative
liaise meticulous mitigate obligatory oversight paradigm
perpetuate predominant rationale reconcile redundant stipulate
stringent substantiate supersede surveillance terminology
transparency unprecedented warranted
""".split())

INFORMAL_WORDS = frozenset("""
awesome cool yeah hey gonna wanna gotta kinda sorta stuff things guys
ok okay yep nope nah dude bro lol wow omg yikes oops
basically totally super pretty much whatever anyway honestly
literally like actually hung chill vibe vibes legit epic
ain't can't won't shouldn't wouldn't couldn't didn't doesn't
y'all gonna lemme dunno alright sick tight dope fire
tbh imo fyi btw bruh fam lowkey highkey sus cap no cap
""".split())

POSITIVE_WORDS = frozenset("""
good great excellent amazing wonderful fantastic incredible awesome brilliant superb
outstanding marvelous terrific fabulous magnificent splendid exceptional remarkable
impressive admirable delightful enjoyable pleasant satisfying gratifying rewarding
beautiful lovely gorgeous stunning attractive charming elegant graceful
happy joyful cheerful merry pleased delighted thrilled excited ecstatic elated
love adore appreciate cherish treasure value respect admire praise
kind generous compassionate caring thoughtful considerate helpful supportive
brave courageous bold daring fearless valiant heroic strong powerful mighty
smart intelligent wise clever brilliant creative innovative resourceful
success successful achievement accomplishment progress improvement advance
hope hopeful optimistic positive confident encouraged motivated inspired
peace peaceful calm serene tranquil harmonious balanced steady stable
trust trustworthy reliable dependable faithful loyal devoted dedicated
free freedom liberty independent empowered capable able skilled talented
fun funny humorous amusing entertaining engaging interesting fascinating
healthy vibrant energetic lively dynamic active fresh pure clean clear
agree approval benefit best better celebrate comfort easy efficient
encourage enhance enthusiastic fortunate friendly gain glad grateful
growth honest honor ideal improve joy lead learn light luck natural nice
open opportunity perfect pleased pride productive profit promote proud
quality recommend refresh safe secure shine simple smooth solve special
strength succeed support sweet triumph unique useful victory warm welcome
win wonderful worth worthy
""".split())

NEGATIVE_WORDS = frozenset("""
bad terrible horrible awful dreadful atrocious abysmal appalling dismal
poor worse worst inferior mediocre substandard inadequate insufficient
ugly hideous grotesque repulsive revolting disgusting repugnant
sad unhappy depressed miserable gloomy melancholy sorrowful grief
hate despise detest loathe abhor resent dislike disapprove reject
cruel harsh mean nasty vicious brutal ruthless merciless callous
weak feeble helpless powerless vulnerable defenseless fragile frail
stupid foolish ignorant dumb idiotic senseless mindless clueless
failure failed failing loss losing defeat decline deterioration setback
fear afraid scared terrified frightened worried anxious nervous
conflict hostile aggressive violent turbulent chaotic unstable volatile
distrust suspicious unreliable unfaithful disloyal treacherous
trapped restricted confined limited constrained oppressed controlled
boring dull tedious monotonous tiresome uninteresting bland
sick unhealthy toxic polluted contaminated corrupt rotten decayed
disagree disapproval damage harm hurt injure destroy ruin waste
anger angry furious enraged irritated annoyed frustrated resentful
blame careless chaotic complain confused costly crisis danger dark
delay deny difficult disappoint disaster doubt empty error evil
excessive excuse exhausting expensive fail fault flawed forbid
guilty ignore impossible impure insane insecure invalid irritate
lack lazy limit lose low misery mistake neglect never nobody
nothing nowhere obstacle odd offend pain panic penalty pitiful
pointless poison poverty pressure problem punish quit refuse
regret ridiculous risk rude scare shame shock stressful struggle
suffer suspect tense threat tragic trouble uncertain unfair unfortunate
unhappy upset useless vague victim violation vulnerable warning
wrong
""".split())
