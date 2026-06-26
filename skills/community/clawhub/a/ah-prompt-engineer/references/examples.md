# Prompt Engineer — Code Examples

## Example 1

```python
import openai
from typing import List, Dict, Any
import json
import re
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    """Structured prompt template with metadata"""
    name: str
    template: str
    variables: List[str]
    category: str
    description: str
    examples: List[Dict[str, Any]]

class PromptEngineer:
    def __init__(self, model_name="gpt-4", temperature=0.1):
        self.model_name = model_name
        self.temperature = temperature
        self.prompt_templates = {}
    
    def create_chain_of_thought_prompt(self, task_description: str, examples: List[Dict]) -> str:
        """Create a chain-of-thought prompt with examples"""
        cot_template = f"""
Task: {task_description}

I'll solve this step by step, showing my reasoning process.

Examples:
"""
        
        for i, example in enumerate(examples, 1):
            cot_template += f"\nExample {i}:\n"
            cot_template += f"Input: {example['input']}\n"
            cot_template += f"Reasoning: {example['reasoning']}\n"
            cot_template += f"Output: {example['output']}\n"
        
        cot_template += "\nNow, let me solve the new problem:\nInput: {input}\nReasoning:"
        
        return cot_template
    
    def create_few_shot_prompt(self, task: str, examples: List[Dict], n_shots: int = 3) -> str:
        """Create few-shot learning prompt"""
        few_shot_template = f"Task: {task}\n\n"
        
        selected_examples = examples[:n_shots]
        for i, example in enumerate(selected_examples, 1):
            few_shot_template += f"Example {i}:\n"
            few_shot_template += f"Input: {example['input']}\n"
            few_shot_template += f"Output: {example['output']}\n\n"
        
        few_shot_template += "Now solve this:\nInput: {input}\nOutput:"
        
        return few_shot_template
    
    def create_role_based_prompt(self, role: str, context: str, task: str) -> str:
        """Create role-based prompt for specific expertise"""
        role_template = f"""
You are a {role}. {context}

Your task is to {task}.

Guidelines:
- Apply your expertise and professional knowledge
- Provide detailed, accurate, and actionable advice
- Consider industry best practices and standards
- Explain your reasoning when necessary

Request: {{input}}

Response:"""
        
        return role_template
    
    def create_structured_output_prompt(self, output_schema: Dict) -> str:
        """Create prompt for structured JSON output"""
        schema_description = json.dumps(output_schema, indent=2)
        
        structured_template = f"""
Please provide your response in the following JSON format:

{schema_description}

Ensure your response is valid JSON and follows the exact schema structure.

Input: {{input}}

JSON Response:"""
        
        return structured_template
    
    def optimize_prompt_iteratively(self, base_prompt: str, test_cases: List[Dict], 
                                  max_iterations: int = 5) -> str:
        """Iteratively optimize prompt based on test results"""
        current_prompt = base_prompt
        best_prompt = base_prompt
        best_score = 0
        
        for iteration in range(max_iterations):
            scores = []
            
            for test_case in test_cases:
                response = self._call_llm(current_prompt.format(**test_case['input']))
                score = self._evaluate_response(response, test_case['expected'])
                scores.append(score)
            
            avg_score = sum(scores) / len(scores)
            
            if avg_score > best_score:
                best_score = avg_score
                best_prompt = current_prompt
            
            # Generate prompt improvements
            if iteration < max_iterations - 1:
                current_prompt = self._improve_prompt(current_prompt, test_cases, scores)
        
        return best_prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM with prompt"""
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        return response.choices[0].message.content
    
    def _evaluate_response(self, response: str, expected: str) -> float:
        """Evaluate response quality (simplified scoring)"""
        # This is a simplified example - in practice, use more sophisticated metrics
        from difflib import SequenceMatcher
        return SequenceMatcher(None, response.lower(), expected.lower()).ratio()
    
    def _improve_prompt(self, prompt: str, test_cases: List[Dict], scores: List[float]) -> str:
        """Generate improved prompt based on performance"""
        improvement_prompt = f"""
Current prompt: {prompt}

Test case performance:
"""
        
        for i, (test_case, score) in enumerate(zip(test_cases, scores)):
            improvement_prompt += f"Test {i+1}: Score {score:.2f}\n"
            improvement_prompt += f"Input: {test_case['input']}\n"
            improvement_prompt += f"Expected: {test_case['expected']}\n\n"
        
        improvement_prompt += """
Please suggest an improved version of the prompt that would perform better on these test cases.
Focus on clarity, specificity, and providing better guidance to the model.

Improved prompt:"""
        
        return self._call_llm(improvement_prompt)

# Advanced prompt templates
PROMPT_TEMPLATES = {
    "code_review": PromptTemplate(
        name="code_review",
        template="""
You are an expert code reviewer with {years} years of experience in {language}.

Review the following code for:
1. Code quality and best practices
2. Potential bugs and security issues
3. Performance optimizations
4. Maintainability and readability

Code to review:
```

## Example 2

```python
import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import numpy as np
from typing import List, Dict, Tuple

class RAGSystem:
    def __init__(self, model_name="gpt-3.5-turbo", embedding_model="text-embedding-ada-002"):
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.retrieval_chain = None
        
    def ingest_documents(self, documents: List[str], chunk_size: int = 1000, 
                        chunk_overlap: int = 200) -> None:
        """Ingest and process documents into vector store"""
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        chunks = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            doc_chunks = text_splitter.split_text(doc)
            chunks.extend(doc_chunks)
            metadatas.extend([{"source": f"doc_{i}", "chunk": j} 
                            for j in range(len(doc_chunks))])
        
        # Create vector store
        self.vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            metadatas=metadatas
        )
        
        # Create retrieval chain
        llm = OpenAI(model_name=self.model_name, temperature=0)
        self.retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 4})
        )
    
    def advanced_retrieval(self, query: str, k: int = 4, 
                          similarity_threshold: float = 0.7) -> List[Dict]:
        """Advanced retrieval with filtering and reranking"""
        # Get initial results
        results = self.vector_store.similarity_search_with_score(query, k=k*2)
        
        # Filter by similarity threshold
        filtered_results = [
            (doc, score) for doc, score in results 
            if score >= similarity_threshold
        ]
        
        # Rerank using query-specific criteria
        reranked_results = self._rerank_results(query, filtered_results)
        
        return reranked_results[:k]
    
    def _rerank_results(self, query: str, results: List[Tuple]) -> List[Dict]:
        """Rerank results based on query context"""
        # Simple reranking based on keyword overlap
        query_words = set(query.lower().split())
        
        scored_results = []
        for doc, similarity_score in results:
            doc_words = set(doc.page_content.lower().split())
            keyword_overlap = len(query_words.intersection(doc_words)) / len(query_words)
            
            # Combined score
            combined_score = 0.7 * similarity_score + 0.3 * keyword_overlap
            
            scored_results.append({
                "document": doc,
                "similarity_score": similarity_score,
                "keyword_overlap": keyword_overlap,
                "combined_score": combined_score
            })
        
        return sorted(scored_results, key=lambda x: x["combined_score"], reverse=True)
    
    def generate_response_with_citations(self, query: str) -> Dict:
        """Generate response with source citations"""
        # Retrieve relevant documents
        relevant_docs = self.advanced_retrieval(query)
        
        # Create context from retrieved documents
        context = "\n\n".join([
            f"Source {i+1}: {doc['document'].page_content}" 
            for i, doc in enumerate(relevant_docs)
        ])
        
        # Create prompt with citations
        prompt = f"""
Context information:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above. 
Include citations in the format [Source X] where X is the source number.

Answer:"""
        
        # Generate response
        llm = OpenAI(model_name=self.model_name, temperature=0.1)
        response = llm(prompt)
        
        return {
            "answer": response,
            "sources": [doc['document'].metadata for doc in relevant_docs],
            "retrieval_scores": [doc['combined_score'] for doc in relevant_docs]
        }
    
    def evaluate_rag_performance(self, test_queries: List[Dict]) -> Dict:
        """Evaluate RAG system performance"""
        metrics = {
            "retrieval_accuracy": [],
            "answer_relevance": [],
            "citation_accuracy": []
        }
        
        for test_case in test_queries:
            query = test_case["query"]
            expected_sources = test_case.get("expected_sources", [])
            expected_answer = test_case.get("expected_answer", "")
            
            # Get response
            response = self.generate_response_with_citations(query)
            
            # Calculate retrieval accuracy
            retrieved_sources = [source["source"] for source in response["sources"]]
            retrieval_accuracy = len(set(retrieved_sources) & set(expected_sources)) / len(expected_sources) if expected_sources else 0
            metrics["retrieval_accuracy"].append(retrieval_accuracy)
            
            # Calculate answer relevance (simplified)
            answer_relevance = self._calculate_answer_relevance(response["answer"], expected_answer)
            metrics["answer_relevance"].append(answer_relevance)
        
        # Calculate average metrics
        return {
            "avg_retrieval_accuracy": np.mean(metrics["retrieval_accuracy"]),
            "avg_answer_relevance": np.mean(metrics["answer_relevance"]),
            "total_queries_tested": len(test_queries)
        }
    
    def _calculate_answer_relevance(self, generated_answer: str, expected_answer: str) -> float:
        """Calculate answer relevance score"""
        # Simplified scoring - in practice, use more sophisticated metrics
        from difflib import SequenceMatcher
        return SequenceMatcher(None, generated_answer.lower(), expected_answer.lower()).ratio()
```

## Example 3

```python
import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, TrainingArguments, 
    Trainer, DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import json
from typing import List, Dict

class LLMFineTuner:
    def __init__(self, base_model: str, use_lora: bool = True):
        self.base_model = base_model
        self.use_lora = use_lora
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = None
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def prepare_training_data(self, data: List[Dict], instruction_format: str = "alpaca") -> Dataset:
        """Prepare training data in instruction format"""
        formatted_data = []
        
        for example in data:
            if instruction_format == "alpaca":
                if "input" in example and example["input"]:
                    formatted_text = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
                else:
                    formatted_text = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{example['instruction']}

### Response:
{example['output']}"""
            
            elif instruction_format == "chat":
                formatted_text = f"""Human: {example['instruction']}

Assistant: {example['output']}"""
            
            formatted_data.append(formatted_text)
        
        # Tokenize data
        tokenized_data = []
        for text in formatted_data:
            tokens = self.tokenizer(text, truncation=True, padding=True, max_length=2048)
            tokenized_data.append(tokens)
        
        return Dataset.from_list(tokenized_data)
    
    def setup_lora_config(self, r: int = 16, lora_alpha: int = 32, target_modules: List[str] = None):
        """Setup LoRA configuration for efficient fine-tuning"""
        if target_modules is None:
            target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
        
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=r,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=0.1
        )
        
        return lora_config
    
    def fine_tune_model(self, train_dataset: Dataset, val_dataset: Dataset = None,
                       output_dir: str = "./fine_tuned_model", epochs: int = 3):
        """Fine-tune the model with training data"""
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Apply LoRA if enabled
        if self.use_lora:
            lora_config = self.setup_lora_config()
            model = get_peft_model(model, lora_config)
            model.print_trainable_parameters()
        
        # Setup training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            evaluation_strategy="steps" if val_dataset else "no",
            eval_steps=100 if val_dataset else None,
            save_steps=500,
            save_total_limit=2
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Setup trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator
        )
        
        # Start training
        trainer.train()
        
        # Save model
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        self.model = model
        return trainer


class PromptEvaluator:
    """Comprehensive prompt evaluation framework"""
    
    def __init__(self):
        self.metrics = {}
    
    def evaluate_generation_quality(self, generated_texts: List[str], 
                                  reference_texts: List[str]) -> Dict:
        """Evaluate text generation quality using multiple metrics"""
        from rouge_score import rouge_scorer
        from bert_score import score
        
        # ROUGE scores
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        rouge_scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
        
        for gen, ref in zip(generated_texts, reference_texts):
            scores = scorer.score(ref, gen)
            rouge_scores['rouge1'].append(scores['rouge1'].fmeasure)
            rouge_scores['rouge2'].append(scores['rouge2'].fmeasure)
            rouge_scores['rougeL'].append(scores['rougeL'].fmeasure)
        
        # BERTScore
        P, R, F1 = score(generated_texts, reference_texts, lang="en")
        
        return {
            'rouge1': np.mean(rouge_scores['rouge1']),
            'rouge2': np.mean(rouge_scores['rouge2']),
            'rougeL': np.mean(rouge_scores['rougeL']),
            'bert_score_precision': P.mean().item(),
            'bert_score_recall': R.mean().item(),
            'bert_score_f1': F1.mean().item()
        }
    
    def evaluate_instruction_following(self, prompts: List[str], responses: List[str]) -> Dict:
        """Evaluate how well the model follows instructions"""
        scores = []
        
        for prompt, response in zip(prompts, responses):
            # Extract instruction from prompt
            instruction = self._extract_instruction(prompt)
            
            # Evaluate instruction following
            score = self._score_instruction_following(instruction, response)
            scores.append(score)
        
        return {
            'avg_instruction_following': np.mean(scores),
            'instruction_following_scores': scores
        }
    
    def _extract_instruction(self, prompt: str) -> str:
        """Extract instruction from prompt"""
        # Simple extraction - in practice, use more sophisticated parsing
        lines = prompt.split('\n')
        for line in lines:
            if 'Instruction:' in line:
                return line.split('Instruction:')[1].strip()
        return prompt
    
    def _score_instruction_following(self, instruction: str, response: str) -> float:
        """Score how well response follows instruction"""
        # Simplified scoring - use LLM-based evaluation in practice
        instruction_words = set(instruction.lower().split())
        response_words = set(response.lower().split())
        
        # Check for key instruction words in response
        overlap = len(instruction_words.intersection(response_words))
        return min(overlap / len(instruction_words), 1.0)


## LangChain Agent Framework
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from langchain.schema import AgentAction, AgentFinish
import re

class CustomPromptTemplate(StringPromptTemplate):
    """Custom prompt template for agents"""
    template: str
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        
        return self.template.format(**kwargs)

class CustomOutputParser:
    """Custom output parser for agent actions"""
    
    def parse(self, llm_output: str):
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        
        action = match.group(1).strip()
        action_input = match.group(2)
        
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

def create_custom_agent():
    """Create a custom LangChain agent with specialized tools"""
    # Define tools
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for searching current information on the internet"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),
            description="Useful for mathematical calculations"
        )
    ]
    
    # Define prompt template
    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""
    
    prompt = CustomPromptTemplate(
        template=template,
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )
    
    # Setup LLM and agent
    llm = OpenAI(temperature=0)
    output_parser = CustomOutputParser()
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=[tool.name for tool in tools]
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )
    
    return agent_executor


## Best Practices
1. **Iterative Refinement**: Continuously test and refine prompts based on results
2. **Context Management**: Maintain appropriate context length and relevance
3. **Safety Measures**: Implement safety filters and content moderation
4. **Evaluation Metrics**: Use comprehensive evaluation frameworks
5. **Version Control**: Track prompt versions and performance metrics
6. **A/B Testing**: Compare different prompt variations systematically
7. **Documentation**: Document prompt design decisions and performance

## Prompt Safety and Alignment
- Implement robust input validation and sanitization
- Use constitutional AI principles for alignment
- Regular safety audits and red team testing
- Monitoring for harmful or biased outputs
- Implementing feedback loops for continuous improvement

## Performance Optimization
- Optimize prompt length vs. performance trade-offs
- Use caching for frequently used prompts
- Implement parallel processing for batch operations
- Monitor latency and cost metrics
- Regular model performance benchmarking

## Approach
- Start with clear objectives and success criteria
- Design systematic evaluation frameworks
- Implement comprehensive testing and validation
- Create modular and reusable prompt components
- Maintain detailed documentation and versioning
- Establish monitoring and feedback mechanisms

## Output Format
- Provide complete prompt engineering frameworks
- Include evaluation and testing methodologies
- Document safety and alignment considerations
- Add performance optimization strategies
- Include deployment and monitoring setups
- Provide comprehensive examples and use cases

---

```
