#!/usr/bin/env python3
"""Agent Coordinator - Multi-agent task coordination.
Distilled from Claude Code Team mode.
"""
import json, sys, os, argparse, threading, time, uuid

class AgentCoordinator:
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        self._lock = threading.Lock()
        self.results = {}

    def decompose_task(self, task_description):
        subtasks = []
        tl = task_description.lower()
        if "analyze" in tl or "\u5206\u6790" in task_description:
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Data collection: "+task_description,"type":"collect"})
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Analysis: "+task_description,"type":"analyze"})
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Report: "+task_description,"type":"report"})
        elif "compare" in tl or "\u5bf9\u6bd4" in task_description:
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Item A: "+task_description,"type":"analyze"})
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Item B: "+task_description,"type":"analyze"})
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":"Comparison: "+task_description,"type":"compare"})
        else:
            subtasks.append({"id":str(uuid.uuid4())[:8],"description":task_description,"type":"general"})
        return subtasks

    def execute_subtask(self, subtask):
        time.sleep(0.1)
        return {"subtask_id":subtask["id"],"status":"completed","type":subtask["type"],"summary":"Result for: "+subtask["description"][:50]}

    def run_parallel(self, subtasks):
        results = []
        def worker(task):
            return self.execute_subtask(task)
        threads = []
        for task in subtasks[:self.max_workers]:
            t = threading.Thread(target=lambda t=task: results.append(worker(t)))
            threads.append(t)
            t.start()
        for t in threads: t.join()
        return results

    def run_pipeline(self, subtasks):
        results = []
        for task in subtasks:
            results.append(self.execute_subtask(task))
        return results

    def ensemble_vote(self, question, num_voters=3):
        votes = []
        for i in range(num_voters):
            time.sleep(0.05)
            vote = {"voter":"agent-"+str(i+1),"vote":"yes" if hash(question+str(i))%2==0 else "no"}
            votes.append(vote)
        yes_count = sum(1 for v in votes if v["vote"]=="yes")
        return {"question":question,"votes":votes,"result":"yes" if yes_count>num_voters/2 else "no","yes":yes_count,"no":num_voters-yes_count}

    def aggregate_results(self, results):
        if not results: return {"status":"no_results"}
        types = {}
        for r in results:
            t = r.get("type","unknown")
            types[t] = types.get(t,0)+1
        return {"status":"completed","total_subtasks":len(results),"completed":sum(1 for r in results if r.get("status")=="completed"),"by_type":types,"summaries":[r.get("summary","") for r in results[:5]]}


def main():
    parser = argparse.ArgumentParser(description="Agent Coordinator")
    parser.add_argument("--task", help="Complex task description")
    parser.add_argument("--subtasks", help="Subtask definitions JSON file")
    parser.add_argument("--workers", type=int, default=3, help="Max parallel workers")
    parser.add_argument("--pipeline", action="store_true", help="Run in pipeline mode")
    parser.add_argument("--ensemble", help="Ensemble vote question")
    parser.add_argument("--voters", type=int, default=3, help="Number of voters")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    coord = AgentCoordinator(max_workers=args.workers)

    if args.ensemble:
        result = coord.ensemble_vote(args.ensemble, args.voters)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("[VOTE] Question: " + result["question"])
            print("  Result: " + result["result"] + " (" + str(result["yes"]) + "/" + str(result["no"]) + ")")
            for v in result["votes"]:
                print("  " + v["voter"] + ": " + v["vote"])
        return

    if args.subtasks:
        with open(args.subtasks,"r",encoding="utf-8") as f: subtasks = json.load(f)
    elif args.task:
        subtasks = coord.decompose_task(args.task)
    else:
        subtasks = []

    if not subtasks:
        print("[?] No subtasks defined")
        return

    if args.pipeline:
        results = coord.run_pipeline(subtasks)
    else:
        results = coord.run_parallel(subtasks)

    aggregated = coord.aggregate_results(results)
    output = {"subtasks": subtasks, "results": results, "aggregated": aggregated}

    if args.export:
        with open(args.export,"w",encoding="utf-8") as f: json.dump(output, f, indent=2, ensure_ascii=False)

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        a = aggregated
        print("[OK] Task completed: " + str(a["total_subtasks"]) + " subtasks, " + str(a["completed"]) + " completed")
        print("  Types: " + str(a["by_type"]))
        for s in a["summaries"]:
            print("  - " + s)


if __name__ == "__main__":
    main()