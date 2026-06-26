// ============================================================================
//  Worked example for the write-custom-activity skill.
//
//  Anonymized: project-neutral. Adapt the namespace, assembly name, and
//  registration metadata to your own publisher / project. All identifiers
//  use the synthetic publisher prefix "ContosoExample".
//
//  Activity: ContosoExample.Substring
//    Input  - String To Parse  (string, required)
//    Input  - Start Position   (int,    required)
//    Input  - Length           (int,    optional - 0 means "to end")
//    Output - Partial String   (string)
//    Output - Failed           (bool,   default false)
//    Output - Failure Message  (string)
//
//  Demonstrates:
//    - Direct CodeActivity derivation (no custom base class).
//    - [Input] / [Output] / [RequiredArgument] / [Default] attribute use.
//    - Argument.Get / Argument.Set with CodeActivityContext.
//    - The Failed / FailureMessage recoverable-error pattern.
//    - The [CrmPluginRegistration] attribute (spkl-style) using the
//      *workflow* constructor (5 args ending in IsolationModeEnum.Sandbox).
//    - Stateless Execute (no instance fields hold runtime data).
//
//  Required NuGet: Microsoft.CrmSdk.Workflow (transitively pulls in
//                  Microsoft.CrmSdk.CoreAssemblies)
//  Target framework: .NET Framework 4.6.2
// ============================================================================

using System;
using System.Activities;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Workflow;

namespace ContosoExample.WorkflowActivities.Strings
{
    [CrmPluginRegistration(
        "ContosoExample: Substring",                   // Name (designer label)
        "ContosoExample: Substring",                   // Friendly Name
        "Return a substring of a given input string.", // Description
        "ContosoExample - Strings",                    // Workflow Activity Group Name (category)
        IsolationModeEnum.Sandbox)]                    // Always Sandbox unless the
                                                       // environment explicitly allows
                                                       // full-trust.
    public sealed class Substring : CodeActivity
    {
        [RequiredArgument]
        [Input("String To Parse")]
        public InArgument<string> StringToParse { get; set; }

        [RequiredArgument]
        [Input("Start Position")]
        public InArgument<int> StartPosition { get; set; }

        // Optional. 0 (the default) means "to the end of the string".
        [Input("Length")]
        [Default("0")]
        public InArgument<int> Length { get; set; }

        [Output("Partial String")]
        public OutArgument<string> PartialString { get; set; }

        [Output("Failed")]
        [Default("false")]
        public OutArgument<bool> Failed { get; set; }

        [Output("Failure Message")]
        public OutArgument<string> FailureMessage { get; set; }

        protected override void Execute(CodeActivityContext context)
        {
            // Pull contextual services. Never cache these on the instance.
            ITracingService tracing = context.GetExtension<ITracingService>();

            tracing.Trace("Entered Substring.Execute()");

            try
            {
                // Read inputs at the top.
                string source       = StringToParse.Get(context) ?? string.Empty;
                int    startIndex   = StartPosition.Get(context);
                int    requested    = Length.Get(context);

                // Defensive bounds-checking. Workflow activities should fail
                // gracefully on bad input — the calling workflow can branch
                // on the Failed output.
                if (startIndex < 0)
                {
                    startIndex = 0;
                }

                if (startIndex > source.Length)
                {
                    tracing.Trace("Start position {0} is past end of source (length {1}).",
                                  startIndex, source.Length);
                    PartialString.Set(context, string.Empty);
                    Failed.Set(context, false);    // not an error — just empty
                    return;
                }

                int available = source.Length - startIndex;
                int take = (requested <= 0 || requested > available)
                    ? available
                    : requested;

                string partial = source.Substring(startIndex, take);

                PartialString.Set(context, partial);
                Failed.Set(context, false);
            }
            catch (Exception ex)
            {
                tracing.Trace("Substring failed: {0}", ex);
                Failed.Set(context, true);
                FailureMessage.Set(context, ex.Message);

                // Recoverable: do NOT rethrow. The caller can branch on
                // Failed. To make this fatal instead, replace the lines
                // above with:
                //     throw new InvalidWorkflowException("Substring failed", ex);
            }
            finally
            {
                tracing.Trace("Exiting Substring.Execute()");
            }
        }
    }
}
