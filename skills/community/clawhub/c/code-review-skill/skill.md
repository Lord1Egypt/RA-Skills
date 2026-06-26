{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;\f1\fnil\fcharset0 Menlo-Bold;}
{\colortbl;\red255\green255\blue255;\red193\green193\blue193;\red24\green24\blue24;\red85\green129\blue224;
\red70\green137\blue204;}
{\*\expandedcolortbl;;\cssrgb\c80000\c80000\c80000;\cssrgb\c12157\c12157\c12157;\cssrgb\c40392\c58824\c90196;
\cssrgb\c33725\c61176\c83922;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Perform a comprehensive code review current staged changes as a senior developer would, focusing on production readiness. Specifically:\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 \strokec4 1.\cf2 \strokec2  
\f1\b \cf5 \strokec5 **Error Handling & Panic Prevention**
\f0\b0 \cf2 \strokec2 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3    \cf4 \strokec4 -\cf2 \strokec2  Review all error paths and ensure none can cause panics\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Check for potential nil pointer dereferences\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Verify that all file operations handle errors gracefully\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Look for any unchecked type assertions or array/slice access that could panic\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 \strokec4 2.\cf2 \strokec2  
\f1\b \cf5 \strokec5 **Production Readiness**
\f0\b0 \cf2 \strokec2 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3    \cf4 \strokec4 -\cf2 \strokec2  Verify logging levels are appropriate (debug vs info vs warn vs error)\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Check if error messages provide sufficient context for debugging\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Ensure the code handles edge cases\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Consider if there are any race conditions or concurrency issues\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 \strokec4 3.\cf2 \strokec2  
\f1\b \cf5 \strokec5 **Code Quality**
\f0\b0 \cf2 \strokec2 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3    \cf4 \strokec4 -\cf2 \strokec2  Look for any code duplication or opportunities for refactoring\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Verify consistent error handling patterns with the rest of the codebase\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Check if variable names are clear and follow Go conventions\cb1 \
\cb3    \cf4 \strokec4 -\cf2 \strokec2  Ensure comments are accurate and helpful\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 \strokec4 4.\cf2 \strokec2  
\f1\b \cf5 \strokec5 **Unit Test**
\f0\b0 \cf2 \strokec2 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3    \cf4 \strokec4 -\cf2 \strokec2  Add a comprehensive unit test for the changes made\cb1 \
\
\cb3 Provide specific code fixes for any issues found, and include the complete unit and component test implementation.\cb1 \
}